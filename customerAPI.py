from flask import Flask, json, jsonify, request, Blueprint, send_file
from flask_httpauth import HTTPBasicAuth
from app import session
import datetime
import pytz
import pymongo
from bson.objectid import ObjectId
import bcrypt
from sqlescapy import sqlescape
import math
import requests

from app import logger

from vicidialAPI import getAllLists, getAllCampaigns

auth = HTTPBasicAuth()

def connectToDB():
    client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mongoDB = client['jamesbon']
    return mongoDB

customerApiBlueprint = Blueprint('customerAPI', __name__)

@auth.verify_password
def verify_password(username, password):
    client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mongoDB = client['jamesbon']
    user_col = mongoDB['users']
    checkUser = user_col.find_one({"email":username})
    password = bytes(password, 'utf-8')
    client.close()
    if checkUser:
        return bcrypt.checkpw(password,bytes(checkUser['password'], 'utf-8'))
    return False

@customerApiBlueprint.route('/api/v2/billing_vici', methods=['GET'])
@auth.login_required
def viciGetBilling():
    if auth.current_user() == 'claude50912@gmail.com':
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        companies_col = mongoDB['companies']
        search_query = {
            'vici_enabled' : True
        }
        return_post = []
        for company in companies_col.find(search_query):
            try:
                charge_per_minute = float(company['billing']['charge_amount'])
            except:
                charge_per_minute = .25
            search_query = {
                'company_id':company['_id']
            }
            wallet_col = mongoDB['company_wallet_balance']
            balance_row = wallet_col.find_one(search_query)
            try:
                balance = getFloatPoint(balance_row['paid_amount'] - balance_row['charge_amount'] + balance_row['refunded_amount'])
            except:
                balance = 0
        
            try:
                charge_per_minute = float(company['billing']['charge_amount'])
            except:
                charge_per_minute = .25


            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            
            url = url_builder(server, 'general_purpose_get', [])
            url += '&user='+user
            url += '&pass='+password

            sql_table = 'vicidial_log'
            column_overide='lead_id,total_seconds,minutes,campaign_id,call_date,phone_number'
            
            campaign_list = getAllCampaigns(str(company['_id']), 'str')
            sql_statement = """
            SELECT lead_id, length_in_sec, CASE  WHEN length_in_sec> 3 THEN CEILING(CAST((length_in_sec) AS INT) / 60) ELSE 0 END as minutes, campaign_id, call_date, phone_number 
            FROM vicidial_log 
            WHERE length_in_sec > 3 and call_date > '{}' and campaign_id in ({})
            """.format(str(datetime.datetime.utcnow())[:-16] + ' 00:00:00', campaign_list)
            url += '&column_overide='+column_overide
            url += '&sql_table='+sql_table
            url += '&sql_query='+sql_statement

            client.close()

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')
            total_minutes = 0
            index = 0
            new_transactions = []
            for x in data:
                try:
                    minutes = int(x['minutes'])
                except:
                    minutes = 0
                total_minutes += minutes
                new_dict = {
                    "company_id":str(company['_id']),
                    "type":"charged",
                    "amount":getFloatPoint(minutes*charge_per_minute),
                    "last_actioned_by":None,
                    "updated_at":str(data[index]['call_date_full']),
                    "created_at":str(datetime.datetime.utcnow())[:-3],
                    "memo":'Campaign ID: ' + str(data[index]['campaign_id']) + ' Lead: ' + str(data[index]['lead_id']) + ' Minutes: ' + str(minutes)
                }
                data[index] = new_dict
                updated_at = datetime.datetime.strptime(new_dict['updated_at'], '%Y-%m-%d %H:%M:%S')
                new_dict['updated_at'] = str(updated_at) + '.000'
                #blah_at = datetime.datetime.strptime(str(datetime.datetime.utcnow())[:-16] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
                blah_at = datetime.datetime.strptime(str(datetime.datetime.utcnow())[:-16] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
                #if created_at > blah_at:
                new_transactions.append(new_dict)
                index += 1

            total_charge = total_minutes*charge_per_minute

            search_query = {
                'company_id':company['_id']
            }
            wallet_col = mongoDB['wallet_transactions']
            balance_rows = wallet_col.find(search_query)
            for x in balance_rows:
                new_dict = {
                    "company_id":str(company['_id']),
                    "type":"charged",
                    "amount":getFloatPoint(x['amount']),
                    "last_actioned_by":None,
                    "created_at":x['created_at'],
                    "updated_at":x['created_at'],
                    "memo":x['memo']
                }
                data.append(new_dict)
            try:
                balance_flag = company['balance_flag']
            except:
                balance_flag = False
            return_post.append({
                'email':str(company['email']),
                'company_name':str(company['name']),
                'company_id':str(company['_id']),
                'balance_flag':balance_flag,
                'balance':getFloatPoint(balance),
                'total_minutes':getFloatPoint(total_minutes),
                'total_charge':getFloatPoint(total_charge),
                'remaining_balance':getFloatPoint(balance-total_charge),
                'data':data,
                'new_transactions':new_transactions
            })
        return jsonify(return_post)
    return jsonify({'Message':'Failure'})

@customerApiBlueprint.route('/api/v2/permissions', methods=['GET'])
@auth.login_required
def permissionsEndpoint():
    if request.method == 'GET':
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        collection_col = mongoDB['permissions']
        limit = 1000
        if request.args.get('limit'):
            try:
                limit = int(request.args.get('limit'))
            except:
                pass
        
        skip = 0
        if request.args.get('skip'):
            try:
                skip = int(request.args.get('skip'))
            except:
                pass

        returnPost = {
            "data":[],
            "user":auth.current_user()
        }
        total_documents = 0
        for row in collection_col.find().skip(skip).limit(limit):
            new_data = convertToJSON(row)
            returnPost["data"].append(new_data)
            total_documents+=1
        returnPost['total_documents'] = total_documents
        client.close()
        return jsonify(returnPost)
    return jsonify({'Message':'Failure'})

@customerApiBlueprint.route('/api/v2/<collection>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.login_required
def universalEndpoint(collection):
    client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mongoDB = client['jamesbon']
    collection_col = mongoDB[collection]
    if collection == 'company_billing':
        return jsonify({'Message':'Failure'})

    if request.method == 'GET':
        #try:
        limit = 1000
        if request.args.get('limit'):
            try:
                limit = int(request.args.get('limit'))
            except:
                pass
        
        skip = 0
        if request.args.get('skip'):
            try:
                skip = int(request.args.get('skip'))
            except:
                pass
        id_list = getAllIds(auth.current_user())
        try:
            new_query = convertQueryToJSON(json.loads(request.args.get('query')))
        except:
            new_query = {}
        returnPost = {
            "data":[],
            "user":auth.current_user()
        }
        total_documents = 0
        if new_query != None:
            for row in collection_col.find(new_query).skip(skip).limit(limit):
                new_data = convertToJSON(row)
                try:
                    if validateJSON(new_data, collection, id_list):
                        returnPost["data"].append(new_data)
                        total_documents+=1
                except:
                    pass
            returnPost['total_documents'] = total_documents
            client.close()
            return jsonify(returnPost)
        else:
            client.close()
            return jsonify({'Message':'Failure'})
        #except:
        #    return jsonify({'Message':'Failure'})
    else:
        if collection == 'wallet_transactions' or collection == 'companies' or collection == 'permissions' or collection == 'leads':
            client.close()
            return jsonify({'Message':'Failure'})
        id_list = getAllIds(auth.current_user())
        returnPost = simpleUpdateRow(collection_col, request.json, request.method, id_list, collection)
        client.close()
        return jsonify(returnPost)

@customerApiBlueprint.route('/api/v2/xfer_number/<token>', methods=['GET'])
def getTransferNumber(token):
    try:
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        virtual_col = mongoDB['virtual_agents']
        filter_by = {
            '_id':ObjectId(token)
        }
        virtual_admin = virtual_col.find_one(filter_by)
        if virtual_admin:
            return jsonify({'number':virtual_admin['xfer']})
        client.close()
    except:
        pass
    return jsonify({'number':'Failure'})

@customerApiBlueprint.route('/api/v2/crm', methods=['POST'])
def testCRM():
    try:
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        crm_col = mongoDB['crm_test']
        try:
            crm_col.insert_one(request.json)
        except:
            #print(str(request.form))
            pass
        client.close()
        return jsonify({'Message':'Success'})
    except:
        pass
    return jsonify({'Message':'Failure'})

def getDecimal(x):
    try:
        return float(x)
    except:
        x = 0
        return float(x)

def getInt(x):
    try:
        return int(x)
    except:
        x = 0

def validateJSON(new_data, collection, id_list):
    try:
        if collection == 'companies':
            if str(new_data['id']) in id_list:
                return True
        elif collection == 'leads' or collection == 'campaign_schedule':
            if str(new_data['campaign_id']) in id_list:
                return True
        else:
            try:
                if str(new_data['company_id']) in id_list:
                    return True
            except:
                pass
            try:
                if str(new_data['role_id']) in id_list:
                    return True
            except:
                pass
            try:
                if str(new_data['_id']) in id_list:
                    return True
            except:
                pass
    except:
        return False
    return False

def getAllIds(email):
    id_list = []
    client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mongoDB = client['jamesbon']
    user_col = mongoDB['users']
    user = user_col.find_one({'email':email})
    if user:
        role_user_col = mongoDB['role_user_new']
        id_list.append(str(user['_id']))
        for role_user in role_user_col.find({'user_id':user['_id']}):
            role_col = mongoDB['roles']
            role = role_col.find_one({'_id':role_user['role_id']})
            id_list.append(str(role_user['role_id']))
            id_list.append(str(role['company_id']))

            campaigns_col = mongoDB['campaigns']
            search_query = {
                'company_id':role['company_id']
            }
            for campaign in campaigns_col.find(search_query):
                id_list.append(str(campaign['_id']))
    client.close()
    return id_list

def convertQueryToJSON(obj):
    objData = {}
    for key in obj:
        if key != 'password':
            if isinstance(obj[key], list):
                objData[key] = []
                thisList = []
                for x in range(0, len(obj[key])):
                    thisDict = {}
                    for listKey in obj[key][x]:
                        try:
                            this_id = ObjectId(obj[key][x][listKey])
                            thisDict[listKey] = this_id
                        except:
                            thisDict[listKey] = obj[key][x][listKey]
                    thisList.append(thisDict)
                
                objData[key] = thisList

            else:
                try:
                    this_id = ObjectId(obj[key])
                    objData[key] = this_id
                except:
                    objData[key] = obj[key]
    try:
        objData['_id'] = objData['id']
        objData.pop('id')
    except:
        pass
    return objData

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

def simpleUpdateRow(collection, data, post_type, id_list, collection_name):
    if post_type == 'POST':
        try:
            _id = None
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
                    if validateJSON(data, collection_name, id_list):
                        _id.append(collection.insert(x))
            else:
                for key in data:
                    if '_id' in key:
                        try:
                            data[key] = ObjectId(data[key])
                        except:
                            data[key] = data[key]
                data['created_at'] = str(datetime.datetime.utcnow())[:-3]
                data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                if validateJSON(data, collection, id_list):
                    _id = collection.insert(data)
            if _id != None:
                return {
                    'Message':'Success',
                    'id':str(_id)
                }
            else:
                return {
                    'Message':'Failure'
                }
        except:
            return {'Message':'Failure'}
    elif post_type == 'PUT':
        try:
            data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
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
            if validateJSON(data, collection_name, id_list):
                collection.update_one({"_id":ObjectId(data['id'])}, updateQuery)
                return {
                    'Message':'Success',
                    'id':data['id']
                }
            return {
                'Message':'Failure'
            }
        except:
            return {'Message':'Failure'}
    elif post_type == 'DELETE':
        try:
            search_query = {}
            for key in data:
                if key == 'id':
                    search_query['_id'] = ObjectId(data[key])
                elif '_id' in key:
                    try:
                        search_query[key] = ObjectId(data[key])
                    except:
                        search_query[key] = data[key]
            if collection.find_one(search_query):
                if validateJSON(search_query, collection_name, id_list):
                    collection.delete_one({"_id":ObjectId(data['id'])})
                    return {
                        'Message':'Success',
                        'id':data['id']
                    }
            return {
                'Message':'Failure'
            }
        except:
            return {'Message':'Failure'}
    return {'Message':'Failure'}

def getFloatPoint(a):
    try:
        x = float("{:.2f}".format(round(a, 2)))
    except:
        x = float("{:.2f}".format(round(0, 2)))
    return x

def url_builder(server, function, params):
    url = '{}/non_agent_api.php?function={}'.format(server, function)
    for param in params:
        url += '&{}={}'.format(param, params[param])
    return url
    
def csv_writer(data, delimiter='|'):
    return_data = []
    try:
        rows = data.split('\n')
        columns = rows[0].split(delimiter)
        del rows[0]
        for row in rows:
            try:
                x = {}
                values = row.split(delimiter)
                for i in range(0, len(columns)):
                    if columns[i] != "":
                        if columns[i] == "length_in_sec":
                            try:
                                x[columns[i]] = int(values[i])
                            except:
                                x[columns[i]] = 0
                        elif columns[i] == "call_date":
                            x['call_date_full'] = values[i]
                            x['call_date'] = str(values[i])[:-9]
                        else:
                            if values[i].isnumeric():
                                if '.' in values[i]:
                                    x[columns[i]] = float(values[i])
                                else:
                                    x[columns[i]] = int(values[i])
                            else:
                                x[columns[i]] = values[i]
                return_data.append(x)
            except:
                pass
    except:
        return_data = {'Message':'Couldn\'t Parse Data'}
    return return_data
