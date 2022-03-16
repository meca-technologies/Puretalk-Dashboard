from bson.objectid import ObjectId
import datetime
from app import session, app
import pytz
from aggrFunctions import *

from twilio.twiml.voice_response import VoiceResponse, Connect, Gather
from twilio.rest import Client
import random
import config

import requests

def unsetCompanyID():
    try:
        session['user']['company_id'] = None
        session.modified = True
    except:
        pass

def validateLogin():
    try:
        if session['user']:
            return True
        else:
            return False
    except:
        return False

def validateCompany(companyID):
    try:
        if str(companyID) in session['companies']:
            return True
    except:
        pass
    return False

def simpleUpdateRow(collection, data, post_type, remote_addr):
    try:
        user_company_id = ObjectId(session['company']['id'])
    except:
        user_company_id = None
    if post_type == 'POST':
        try:
            if isinstance(data, list):
                for x in data:
                    for key in x:
                        if '_id' in key:
                            try:
                                x[key] = ObjectId(x[key])
                            except:
                                x[key] = x[key]
                        else:
                            x[key] = x[key]
                    x['created_at'] = str(datetime.datetime.utcnow())[:-3]
                    x['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                    try:
                        x['updated_by'] = ObjectId(session['user']['user_id'])
                    except:
                        x['updated_by'] = ObjectId('613b8a785a2cd24ac1a33bc0')
                    _id = collection.insert(x)
                    try:
                        mongoDB = app.mongo_client['logs']
                        collections_log_col = mongoDB['collections']
                        insert_query = {
                            'user_id':ObjectId(session['user']['user_id']),
                            'company_id':user_company_id,
                            'query':x,
                            'type':'INSERT',
                            'collection':collection.__dict__['_Collection__name'],
                            'ip': remote_addr[0],
                            'created_at':str(datetime.datetime.utcnow())[:-3]
                        }
                        collections_log_col.insert(insert_query)
                    except:
                        pass
            else:
                for key in data:
                    if '_id' in key:
                        try:
                            data[key] = ObjectId(data[key])
                        except:
                            data[key] = data[key]
                data['created_at'] = str(datetime.datetime.utcnow())[:-3]
                data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                try:
                    data['updated_by'] = ObjectId(session['user']['user_id'])
                except:
                    data['updated_by'] = ObjectId('613b8a785a2cd24ac1a33bc0')
                _id = collection.insert(data)
                try:
                    mongoDB = app.mongo_client['logs']
                    collections_log_col = mongoDB['collections']
                    insert_query = {
                        'user_id':ObjectId(session['user']['user_id']),
                        'company_id':user_company_id,
                        'query':data,
                        'type':'INSERT',
                        'collection':collection.__dict__['_Collection__name'],
                        'ip': remote_addr[0],
                        'created_at':str(datetime.datetime.utcnow())[:-3]
                    }
                    collections_log_col.insert(insert_query)
                except:
                    pass
            return {
                'Message':'Success',
                'id':str(_id)
            }
        except:
            return {'Message':'Failure'}
    elif post_type == 'PUT':
        try:
            try:
                if data['updated_at'] == None:
                    data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
            except:
                data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
            
            try:
                data['updated_by'] = ObjectId(session['user']['user_id'])
            except:
                data['updated_by'] = ObjectId('613b8a785a2cd24ac1a33bc0')

            updateQuery = {
                "$set":{}
            }
            for key in data:
                if '_id' in key:
                    try:
                        updateQuery["$set"][key]  = ObjectId(data[key])
                    except:
                        updateQuery["$set"][key]  = data[key]
                elif key != 'id':
                    updateQuery["$set"][key] = data[key]
                else:
                    updateQuery["$set"][key] = data[key]
            search_query = {
                "_id":ObjectId(data['id'])
            }
            collection.update_one(search_query, updateQuery)
            try:
                mongoDB = app.mongo_client['logs']
                collections_log_col = mongoDB['collections']
                insert_query = {
                    'user_id':ObjectId(session['user']['user_id']),
                    'company_id':user_company_id,
                    'query':data,
                    'type':'UPDATE',
                    'collection':collection.__dict__['_Collection__name'],
                    'ip': remote_addr[0],
                    'created_at':str(datetime.datetime.utcnow())[:-3]
                }
                collections_log_col.insert(insert_query)
            except:
                pass
            return {
                'Message':'Success',
                'id':data['id']
            }
        except:
            return {'Message':'Failure'}
    elif post_type == 'DELETE':
        try:
            collection.delete_one({"_id":ObjectId(data['id'])})
            try:
                mongoDB = app.mongo_client['logs']
                collections_log_col = mongoDB['collections']
                insert_query = {
                    'user_id':ObjectId(session['user']['user_id']),
                    'company_id':user_company_id,
                    'query':data,
                    'type':'DELETE',
                    'collection':collection.__dict__['_Collection__name'],
                    'ip': remote_addr[0],
                    'created_at':str(datetime.datetime.utcnow())[:-3]
                }
                collections_log_col.insert(insert_query)
            except:
                pass
            return {
                'Message':'Success',
                'id':data['id']
            }
        except:
            return {'Message':'Failure'}
    return {'Message':'Failure'}

def convertToJSON(obj):
    objData = {}
    for key in obj:
        if key != 'password':
            if isinstance(obj[key], list):
                objData[key] = []
                thisList = []
                for x in range(0, len(obj[key])):
                    thisDict = {}
                    for listKey in obj[key][x]:
                        if isinstance(obj[key][x][listKey], str):
                            thisDict[listKey] = str(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], bytes):
                            thisDict[listKey] = str(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], bool):
                            thisDict[listKey] = obj[key][x][listKey]
                        elif isinstance(obj[key][x][listKey], int):
                            thisDict[listKey] = getInt(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], float):
                            thisDict[listKey] = getDecimal(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], ObjectId):
                            thisDict[listKey] = str(obj[key][x][listKey])
                        else:
                            thisDict[listKey] = obj[key][x][listKey]
                    thisList.append(thisDict)
                
                objData[key] = thisList

            else:
                if isinstance(obj[key], str):
                    objData[key] = str(obj[key])
                elif isinstance(obj[key], bytes):
                    objData[key] = str(obj[key])
                elif isinstance(obj[key], bool):
                    objData[key] = obj[key]
                elif isinstance(obj[key], int):
                    objData[key] = getInt(obj[key])
                elif isinstance(obj[key], float):
                    objData[key] = getDecimal(obj[key])
                elif isinstance(obj[key], ObjectId):
                    objData[key] = str(obj[key])
                else:
                    objData[key] = obj[key]
    try:
        objData['id'] = objData['_id']
        objData.pop('_id')
    except:
        pass
    return objData

def tz_diff(home):
    utcnow = pytz.timezone('utc').localize(datetime.datetime.utcnow()) # generic time
    here = utcnow.astimezone(pytz.timezone(home)).replace(tzinfo=None)
    there = utcnow.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)

    offset = relativedelta(there,here)
    return(offset.hours)

## THIS FUNCTION WORKS BY REFERENCING TWO DICTIONARIES WE HAVE SAVED 
## ONE IS FOR STORING ALL AREA CODES AND WHICH TIMEZONE AND STATE THEY BELONG TO
## THE OTHER IS FOR STORING STATE LAWS ABOUT AUTO DIAL TIMES
## WE GRAB THE PHONE NUMBER AND TAKE THE AREA CODE OUT OF THAT
## THEN WE FIND WHAT STATE IT BELONGS TO
## LASTLY WE CHECK THE LAWS FOR WHAT TIME WE CAN CALL FOR THAT STATE AND WHAT DAY IT IS NOW IN THAT TIMEZONE
## WE RETURN TRUE OR FALSE OF WHETHER OR NOT WE CAN MAKE THE CALL
def phone_tz_check(phoneNumber):
    try:
        utcnow = pytz.timezone('utc').localize(datetime.datetime.utcnow()) # generic time

        areaCode = phoneNumber[2:5]
        state = None
        tz = None
        startTime = None
        endTime = None
        for area in areaCodeTZ:
            if str(area['area_code']) == areaCode:
                state = area['state']
                tz = area['time_zone']
                break
        here = utcnow.astimezone(pytz.timezone(tz)).replace(tzinfo=None)
        day = here.weekday()
        for law in stateLaws:
            if law['State'] == state:
                enabled = law['days'][day]['allowed']
                startTime = law['days'][day]['start_full']
                endTime = law['days'][day]['end_full']
                break

        if enabled == 0:
            return False

        startHour = startTime.split(':')[0]
        startMin = startTime.split(':')[1]

        endHour = endTime.split(':')[0]
        endMin = endTime.split(':')[1]
        startTime = here.replace(hour=int(startHour), minute=int(startMin))
        endTime = here.replace(hour=int(endHour), minute=int(endMin))

        if here >= startTime and here < endTime:
            return True
        return False
    except:
        return True

def formatDate(myDate):
    return myDate.strftime("%Y/%m/%d")
    
def formatNiceDate(myDate):
    return myDate.strftime("%m/%d/%Y")

def formatDateStd(myDate):
    return myDate.strftime("%Y-%m-%d")

def getDecimal(x):
    try:
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return float(x)
    except:
        x = 0
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return float(x)

def getInt(x):
    try:
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)
    except:
        x = 0
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)

def formatStringToJSON(x):
    x = str((x).decode("utf-8"))
    leadData = None
    try:
        leadData = json.loads(x)
        print('Properly Loaded')
        return json.loads(leadData)
    except:
        try:
            leadData = str(x).replace("'\"", "'\\\"")
            leadData = str(leadData).replace("\"'", "\\\"'")
            leadData = str(leadData).replace("'", '"')
            return json.loads(leadData)
        except:
            leadData = str(x).replace("'\"", "'\\\"")
            leadData = str(leadData).replace("\"'", "\\\"'")
            leadData = str(leadData).replace("'", '"')
    return None