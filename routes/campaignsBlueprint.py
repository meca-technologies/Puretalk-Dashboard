from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *
import config

campaignsBlueprint = Blueprint('campaignsAPI', __name__)

@campaignsBlueprint.route('/api/v1/campaigns', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaigns_col = mongoDB['campaigns']
        if request.method == 'GET':
            #try:
            filterBy = {}
            if request.args.get('campaignid'):
                filterBy['_id'] = ObjectId(request.args.get('campaignid'))

            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    filterBy['company_id'] = ObjectId(request.args.get('companyid'))
            try:
                if session['user']['company_id']:
                    filterBy['company_id'] = ObjectId(session['user']['company_id'])
                elif session['companies']:
                    filterBy['company_id'] = {
                        "$in":[]
                    }
                    for company in session['companies']:
                        filterBy['company_id']['$in'].append(ObjectId(company))
            except:
                pass

            if request.args.get('status'):
                filterBy['status'] = request.args.get('status')

            if request.args.get('created_by'):
                filterBy['created_by'] = request.args.get('created_by')
            
            limit = 10
            if request.args.get('limit'):
                try:
                    limit = int(request.args.get('limit'))
                except:
                    pass

            returnPost = []
            for campaign in campaigns_col.find(filterBy):
                userData = []
                users_col = mongoDB['users']
                for user in users_col.find({'company_id':campaign['company_id']}):
                    compaign_user_col = mongoDB['users']
                    if compaign_user_col.find_one({'user_id':user['_id']}):
                        userData.append({
                            'user_id':str(user['_id']),
                            'first_name':user['first_name'],
                            'last_name':user['last_name'],
                            'enabled':True
                        })
                    else:
                        userData.append({
                            'user_id':str(user['_id']),
                            'first_name':user['first_name'],
                            'last_name':user['last_name'],
                            'enabled':False
                        })

                campaignData = convertToJSON(campaign)

                campaignData['leads'] = []
                campaignData['user_data'] = userData
                campaignData['schedules'] = {}
                
                if request.args.get('summary'):
                    leads_total_summary_col = mongoDB['leads_total_summary']
                    summaryFilterBy = {
                        'campaign_id':campaign['_id']
                    }
                    lead_summary = leads_total_summary_col.find_one(summaryFilterBy)
                    try:
                        campaignData['total_leads'] = getInt(lead_summary['total_leads'])
                        campaignData['remaining_leads'] = getInt(lead_summary['remaining_leads'])
                    except:
                        campaignData['total_leads'] = 0
                        campaignData['remaining_leads'] = 0

                if request.args.get('campaignid'):
                    # JUST BASE DATA FOR DEFAULTS
                    campaignData['schedules'] = {
                                "friday": {
                                    "enabled": True,
                                    "start": {
                                        "campaign_id": 63,
                                        "day_value": "friday",
                                        "enabled": True,
                                        "hour": 9,
                                        "id": 13,
                                        "minute": 0,
                                        "status": "start",
                                        "time_full": "09:00:00"
                                    },
                                    "stop": {
                                        "campaign_id": 63,
                                        "day_value": "friday",
                                        "enabled": True,
                                        "hour": 17,
                                        "id": 14,
                                        "minute": 0,
                                        "status": "stop",
                                        "time_full": "17:00:00"
                                    }
                                },
                                "monday": {
                                    "enabled": True,
                                    "start": {
                                        "campaign_id": 63,
                                        "day_value": "monday",
                                        "enabled": True,
                                        "hour": 9,
                                        "id": 5,
                                        "minute": 0,
                                        "status": "start",
                                        "time_full": "09:00:00"
                                    },
                                    "stop": {
                                        "campaign_id": 63,
                                        "day_value": "monday",
                                        "enabled": True,
                                        "hour": 17,
                                        "id": 6,
                                        "minute": 0,
                                        "status": "stop",
                                        "time_full": "17:00:00"
                                    }
                                },
                                "saturday": {
                                    "enabled": False,
                                    "start": {
                                        "campaign_id": 63,
                                        "day_value": "saturday",
                                        "enabled": False,
                                        "hour": 9,
                                        "id": 15,
                                        "minute": 0,
                                        "status": "start",
                                        "time_full": "09:00:00"
                                    },
                                    "stop": {
                                        "campaign_id": 63,
                                        "day_value": "saturday",
                                        "enabled": False,
                                        "hour": 17,
                                        "id": 16,
                                        "minute": 0,
                                        "status": "stop",
                                        "time_full": "17:00:00"
                                    }
                                },
                                "sunday": {
                                    "enabled": False,
                                    "start": {
                                        "campaign_id": 63,
                                        "day_value": "sunday",
                                        "enabled": False,
                                        "hour": 9,
                                        "id": 3,
                                        "minute": 0,
                                        "status": "start",
                                        "time_full": "09:00:00"
                                    },
                                    "stop": {
                                        "campaign_id": 63,
                                        "day_value": "sunday",
                                        "enabled": False,
                                        "hour": 17,
                                        "id": 4,
                                        "minute": 0,
                                        "status": "stop",
                                        "time_full": "17:00:00"
                                    }
                                },
                                "thursday": {
                                    "enabled": True,
                                    "start": {
                                        "campaign_id": 63,
                                        "day_value": "thursday",
                                        "enabled": True,
                                        "hour": 9,
                                        "id": 11,
                                        "minute": 0,
                                        "status": "start",
                                        "time_full": "09:00:00"
                                    },
                                    "stop": {
                                        "campaign_id": 63,
                                        "day_value": "thursday",
                                        "enabled": True,
                                        "hour": 17,
                                        "id": 12,
                                        "minute": 0,
                                        "status": "stop",
                                        "time_full": "17:00:00"
                                    }
                                },
                                "tuesday": {
                                    "enabled": True,
                                    "start": {
                                        "campaign_id": 63,
                                        "day_value": "tuesday",
                                        "enabled": True,
                                        "hour": 9,
                                        "id": 7,
                                        "minute": 0,
                                        "status": "start",
                                        "time_full": "09:00:00"
                                    },
                                    "stop": {
                                        "campaign_id": 63,
                                        "day_value": "tuesday",
                                        "enabled": True,
                                        "hour": 17,
                                        "id": 8,
                                        "minute": 0,
                                        "status": "stop",
                                        "time_full": "17:00:00"
                                    }
                                },
                                "wednesday": {
                                    "enabled": True,
                                    "start": {
                                        "campaign_id": 63,
                                        "day_value": "wednesday",
                                        "enabled": True,
                                        "hour": 9,
                                        "id": 9,
                                        "minute": 0,
                                        "status": "start",
                                        "time_full": "09:00:00"
                                    },
                                    "stop": {
                                        "campaign_id": 63,
                                        "day_value": "wednesday",
                                        "enabled": True,
                                        "hour": 17,
                                        "id": 10,
                                        "minute": 0,
                                        "status": "stop",
                                        "time_full": "17:00:00"
                                    }
                                }
                            }
                    scheduleFilterBy = {
                        'campaign_id':ObjectId(request.args.get('campaignid'))
                    }
                    schedule_col = mongoDB['campaign_schedule']
                    for schedule in schedule_col.find(scheduleFilterBy):
                        if not campaignData['schedules'].get(schedule['day_value']):
                            campaignData['schedules'][schedule['day_value']] = {}
                        
                        users_col = mongoDB['users']
                        loggedInUser = users_col.find_one({'_id':ObjectId(session['user']['user_id'])})

                        ## THIS IS FOR CONVERTING TIMES TO LOCAL TIME FOR THE LOGGED IN USER ##
                        source_date = datetime.datetime.now()
                        source_time_zone = pytz.timezone('UTC')
                        source_date = source_date.replace(hour=schedule['hour'], minute=schedule['minute'])
                        source_date_with_timezone = source_time_zone.localize(source_date)

                        ## WE THEN CONVERT IT TO THE TIMEZONE OF THE LOGGED IN USER ##
                        target_time_zone = pytz.timezone(loggedInUser['timezone'])
                        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
                        campaignData['schedules'][schedule['day_value']][schedule['status']] = {
                            "id":str(schedule['_id']),
                            "campaign_id":str(schedule['campaign_id']),
                            "day_value":schedule['day_value'],
                            "status":schedule['status'],
                            "time_full":str(target_date_with_timezone.strftime('%H:%M')),
                            "hour":int(target_date_with_timezone.strftime('%H')),
                            "minute":int(target_date_with_timezone.strftime('%M')),
                            "enabled":schedule['enabled']
                        }
                        campaignData['schedules'][schedule['day_value']]['enabled'] = schedule['enabled']

                returnPost.append(campaignData)
            
            #client.close()
            return jsonify(returnPost)
            #except:
            #    return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                
                try:
                    users = postData['user_data']
                except:
                    users = None
                try:
                    if session['user']['company_id']:
                        postData['company_id'] = session['user']['company_id']
                except:
                    pass
                returnData = simpleUpdateRow(campaigns_col, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))

                #if users:
                #    campaignID = returnData['id']
                #    campaign_member_col = mongoDB['campaign_members']
                #    for user in users:
                #        user['campaign_id'] = campaignID
                #        simpleUpdateRow(campaign_member_col, user, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'PUT':
            try:
                updateData = request.json
                try:
                    schedules = updateData['schedule_data']
                    updateData.pop('schedule_data')
                except:
                    schedules = None
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                returnData = simpleUpdateRow(campaigns_col, updateData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))

                if schedules:
                    for schedule in schedules:
                        try:
                            users_col = mongoDB['users']
                            loggedInUser = users_col.find_one({'_id':ObjectId(session['user']['user_id'])})

                            ## THIS IS FOR CONVERTING TIMES TO LOCAL TIME FOR THE LOGGED IN USER ##
                            time_full = datetime.datetime.strptime(schedule['time_full'], '%H:%M:%S')
                            offsetHours = tz_diff(loggedInUser['timezone'])
                            source_date = time_full.replace(hour=time_full.hour+offsetHours, minute=time_full.minute, second=0)

                            schedule['hour'] = int(source_date.strftime('%H'))
                            schedule['minute'] = int(source_date.strftime('%M'))
                            schedule['time_full'] = str(source_date.strftime('%H:%M:%S'))
                            schedule['campaign_id'] = updateData['id']
                            filterBy = {
                                'campaign_id':ObjectId(updateData['id']),
                                'day_value':schedule['day_value'],
                                'status':schedule['status']
                            }
                            campaign_schedule_col = mongoDB['campaign_schedule']
                            updateRow = campaign_schedule_col.find_one(filterBy)
                            if updateRow:
                                schedule['id'] = str(updateRow['_id'])
                                schedule['campaign_id'] = ObjectId(updateData['id'])
                                returnData = simpleUpdateRow(campaign_schedule_col, schedule, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                            else:
                                schedule['campaign_id'] = ObjectId(updateData['id'])
                                time_full = str(source_date.strftime('%H:%M:%S'))
                                schedule['hour'] = int(source_date.strftime('%H'))
                                schedule['minute'] = int(source_date.strftime('%M'))
                                
                                returnData = simpleUpdateRow(campaign_schedule_col, schedule, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                        except:
                            pass          
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'DELETE':
            #client.close()
            return jsonify(simpleUpdateRow(campaigns_col, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(',')))

@campaignsBlueprint.route('/api/v1/campaigns/caller-ids', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignCallerIDsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        company_caller_ids_col = mongoDB['company_caller_ids']
        if request.method == 'GET':
            try:
                filterBy = {}
                valid = False
                if request.args.get('companyid'):
                    filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    valid = True
                else:
                    filterBy['company_id'] = ObjectId(session['company']['id'])
                    valid = True

                if request.args.get('callerid'):
                    filterBy['_id'] = ObjectId(request.args.get('callerid'))
                    valid = True
                
                if valid == False:
                    return jsonify({'Message':'Failure'})

                returnPost = []
                print(filterBy)
                for caller in company_caller_ids_col.find(filterBy):
                    callerData = convertToJSON(caller)
                    returnPost.append(callerData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            #try:
            postDataList = request.json

            companyID = session['company']['id']
            currList = []
            for caller in company_caller_ids_col.find({'company_id':ObjectId(companyID)}):
                currList.append(caller['caller_id'])

            filteredList = []
            for postData in postDataList:
                print(postData)
                if postData['caller_id'] not in currList:
                    postData['company_id'] = ObjectId(companyID)
                    filteredList.append(postData)

            returnPost = simpleUpdateRow(company_caller_ids_col, filteredList, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            #client.close()
            return jsonify(returnPost)
            #except:
            #    return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            returnPost = simpleUpdateRow(company_caller_ids_col, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            #client.close()
            return jsonify(returnPost)

@campaignsBlueprint.route('/api/v1/campaigns/caller-ids/verify', methods=['GET','POST'])
def campaignCallerIDsVerifyAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaign_caller_ids_verify_col = mongoDB['caller_id_verifications']
        if request.method == 'GET':
            filterBy = {}
            if request.args.get('callerid'):
                filterBy['caller_id'] = ObjectId(request.args.get('callerid'))
            print(filterBy)
            verification_row = campaign_caller_ids_verify_col.find_one(filterBy)
            #verificationRow = CallerIDVerifications.query.filter_by(**filterBy).first()
            #client.close()
            return verification_row['status']

        elif request.method == 'POST':
            postDataList = request.json
            company_caller_ids_col = mongoDB['company_caller_ids']
            callerRow = company_caller_ids_col.find_one({'_id':ObjectId(postDataList['id'])})
            company_col = mongoDB['companies']
            company = company_col.find_one({'_id':ObjectId(callerRow['company_id'])})

            account_sid = company['twilio_account_sid']
            auth_token = company['twilio_auth_token']
            
            ref_num = ''.join(filter(str.isdigit, callerRow['caller_id']))
            if len(ref_num) == 10:
                ref_num = '+1'+ref_num
            try:
                friendly_name = callerRow['name']
            except:
                friendly_name = str(ref_num)
            twilClient = Client(account_sid, auth_token)
            validation_request = twilClient.validation_requests.create(
                friendly_name=friendly_name,
                status_callback='{}/api/v1/campaigns/caller-ids/verify/hook'.format(config.hostname),
                phone_number=ref_num
            )
            
            newRowData = {
                "caller_id":postDataList['id'],
                "verification_code":str(validation_request.validation_code),
                "account_sid":account_sid,
                "caller_id_number":ref_num,
                'status':'incomplete'
            }
            simpleUpdateRow(campaign_caller_ids_verify_col, newRowData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            newRowData['caller_id'] = str(newRowData['caller_id'])
            newRowData['_id'] = str(newRowData['_id'])
            #client.close()
            return jsonify(newRowData)

@campaignsBlueprint.route('/api/v1/campaigns/caller-ids/verify/hook', methods=['POST'])
def campaignCallerIDsVerifyHookAPI():
    filterBy = {
        'account_sid':request.form.get('AccountSid'),
        'caller_id_number':request.form.get('Called'),
        'status':'incomplete'
    }

    #client = app.mongo_client
    mongoDB = app.mongo_client['jamesbon']
    campaign_caller_ids_verify_col = mongoDB['caller_id_verifications']
    campaign_caller_ids_verify_col.update_one(filterBy, { "$set": { "status" : request.form.get('VerificationStatus') } })

    if request.form.get('VerificationStatus') == 'success':
        filterBy = {
            'account_sid':request.form.get('AccountSid'),
            'caller_id_number':request.form.get('Called'),
            'status':'success'
        }
        verification_row = campaign_caller_ids_verify_col.find_one(filterBy)
        campaign_caller_ids_col = mongoDB['company_caller_ids']
        campaign_caller_ids_col.update_one({"_id":verification_row['caller_id']}, { "$set": { "verified" : True } })
    #client.close()
    return jsonify({"Message":"Success"})

@campaignsBlueprint.route('/api/v1/campaigns/counts')
def campaignCountsAPI():
    if validateLogin():
        #try:
        if True:
            filterBy = {
                'status': {
                    '$ne':'completed'
                }
            }

            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    filterBy['company_id'] = ObjectId(request.args.get('companyid'))

            try:
                if session['user']['company_id']:
                    filterBy['company_id'] = ObjectId(session['user']['company_id'])
            except:
                pass
            
            limit = 10
            if request.args.get('limit'):
                try:
                    limit = int(request.args.get('limit'))
                except:
                    pass

            returnPost = []

            campaign_list = {}
            campaign_ids = []
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            campaigns_col = mongoDB['campaigns']
            for campaign in campaigns_col.find(filterBy):
                campaign_list[str(campaign['_id'])] = {
                    "id":campaign['_id'],
                    "name":campaign['name'],
                    "status":campaign['status']
                }
                campaign_ids.append(campaign['_id'])
            
            filterBy = {
                "campaign_id": {
                    "$in":campaign_ids
                }
            }
            returnPost = []
            leads_col = mongoDB['leads']
            pipeline = leads_interest_summary(filterBy)
            for campaign in leads_col.aggregate(pipeline):
                print(campaign)
                returnPost.append({
                    "interested": campaign['total_interested'], 
                    "name": campaign_list[str(campaign['campaign_id'])]['name'], 
                    "not_interested": campaign['total_uninterested']
                })
            #client.close()
            return jsonify(returnPost)
        #except:
        #    return jsonify({'Message':'Failure'})

@campaignsBlueprint.route('/api/v1/campaigns/make-call', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignCallerAPI():
    if validateLogin():
        if request.method == 'POST':
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads_col = mongoDB['leads']
            try:
                postData = request.json
                phoneNames = ['Phone','phone','Phone Number','phone number','Phone No.','phone no.','Phone No','phone no','cell phone number','Cell Phone Number','contact number','Contact Number','Contact No.','Mobile','mobile','Mobile No',' mobile no','Mobile Number','mobile number','Customer Number','customer number','Customer number','customer Number', 'Telephone No', 'Telephone', 'telephone no', 'telephone', 'Telephone Number' , 'telephone number']
                
                refNum = None
                for x in postData['lead_data']:
                    if str(x['field_name']) in phoneNames:
                        refNum = ''.join(filter(str.isdigit, x['field_value']))
                        if len(refNum) == 10:
                            refNum = '+1'+refNum

                if refNum:
                    try:
                        leadID = ObjectId(postData['lead_id'])
                    except:
                        leadID = None
                    if leadID == None:
                        leadRow = leads_col.find_one({'campaign_id':ObjectId(postData['campaign_id']), 'reference_number':refNum})
                        if leadRow:
                            leadID = leadRow['_id']
                            updateData = {
                                'id':leadID,
                                'lead_data':postData['lead_data']
                            }
                            simpleUpdateRow(leads_col, updateData, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                        if leadID == None:
                            updateData = {
                                'reference_number':refNum,
                                'campaign_id':ObjectId(postData['campaign_id']),
                                'lead_data':postData['lead_data'],
                                'call_logs':[],
                                'status':'unactioned',
                                'updated_at':str(datetime.datetime.utcnow())[:-7]
                            }
                            
                            newRow = simpleUpdateRow(leads_col, updateData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                            leadID = newRow['id']
                    else:
                        leadRow = leads_col.find_one({'_id':leadID})
                        refNum = ''.join(filter(str.isdigit, leadRow['reference_number']))
                        if len(refNum) == 10:
                            refNum = '+1'+refNum
                    campaign_col = mongoDB['campaigns']
                    campaign = campaign_col.find_one({'_id':ObjectId(postData['campaign_id'])})
                    if campaign:
                        company_col = mongoDB['companies']
                        company = company_col.find_one({'_id':campaign['company_id']})
                        account_sid = company['twilio_account_sid']
                        auth_token = company['twilio_auth_token']
                        virtual_agent_col = mongoDB['virtual_agents']
                        try:
                            virtual_agent = virtual_agent_col.find_one({'_id':campaign['virtual_agent_id']})
                        except:
                            print('No AI')
                            return jsonify({'Message':'Failure', 'Error':'No Virtual Agent Attached'})
                        if virtual_agent:
                            # GRAB CALLER ID
                            try:
                                caller_id = postData['caller_id']
                            except:
                                caller_ids = campaign['caller_ids']
                                print(caller_ids)
                                caller_id = caller_ids[0]['caller_id']

                            account_sid = account_sid
                            auth_token = auth_token
                            twilClient = Client(account_sid, auth_token)
                            company_wallet_balance_col = mongoDB['company_wallet_balance']
                            filterBy = {
                                'company_id':campaign['company_id']
                            }
                            company_wallet_balance = company_wallet_balance_col.find_one(filterBy)
                            if company_wallet_balance == None:
                                return jsonify({'Message':'Failure', 'Error':'Insufficient Funds'})
                            returnBalance = {
                                "paid_balance":getDecimal(company_wallet_balance['paid_amount']),
                                "refunded_balance":getDecimal(company_wallet_balance['refunded_amount']),
                                "charged_balance":getDecimal(company_wallet_balance['charge_amount'])
                            }
                            returnBalance['balance'] = returnBalance['paid_balance'] - returnBalance['refunded_balance'] - returnBalance['charged_balance']
                            if returnBalance['balance']  > .5:
                                try:
                                    call = twilClient.calls.create(
                                                            timeout=28,
                                                            application_sid=virtual_agent['app_id'],
                                                            to=refNum,
                                                            from_=caller_id,
                                                            caller_id=caller_id,
                                                            record=True,
                                                            recording_status_callback='{}recording/callback'.format(config.webhooks),
                                                            recording_status_callback_method='POST'
                                                    )
                                except Exception as e: 
                                    errors = str(e).split('\n')
                                    error_message = errors[7]
                                    error_message = error_message.replace('[34m[49m', '')
                                    error_message = error_message.replace('[0m', '')
                                    return jsonify({'Message':'Failure', 'Error':error_message})
                                updateData = {
                                    'id':str(leadID),
                                    'status':'calling',
                                    'updated_at':str(datetime.datetime.utcnow())[:-7]
                                }
                                simpleUpdateRow(leads_col, updateData, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                                updateQuery = {
                                    "$push":{
                                        "call_logs":{
                                            'lead_id':leadID,
                                            'call_id':str(call.sid),
                                            'reference_number':refNum,
                                            'status':'calling',
                                            'created_at':str(datetime.datetime.utcnow())[:-7],
                                            'updated_at':str(datetime.datetime.utcnow())[:-7]
                                        }
                                    }
                                }
                                leads_col.update_one({'_id':leadID}, updateQuery)
                            else:
                                return jsonify({'Message':'Failure', 'Error':'Insufficient Funds'})
                        else:
                            return jsonify({'Message':'Failure', 'Error':'No Virtual Agent Attached'})
                    else:
                        return jsonify({'Message':'Failure', 'Error':'No Campaign Selected'})
                else:
                    return jsonify({'Message':'Failure', 'Error':'No Phone Number Provided'})
            except Exception as e:
                print(e)
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@campaignsBlueprint.route('/api/v1/campaigns/test-hook', methods=['POST'])
def campaignTestHookAPI():
    try:
        if validateLogin():
            if request.method == 'POST':
                post_data = request.json
                
                # TEST VARIABLES PASSED
                request_payload = json.loads(post_data['request_payload'])
                request_url = post_data['request_url']

                # HEADER WORK ##########################################
                request_headers = post_data['request_headers']
                request_headers = delimiterReplace(str(request_headers), request_payload)
                request_headers = json.loads(request_headers.replace("'", '"'))
                req_headers = {}
                for header in request_headers:
                    req_headers[header['field']] = header['value']

                # PARAMS WORK ##########################################
                request_params = post_data['request_params']
                request_params = delimiterReplace(str(request_params), request_payload)
                request_params = json.loads(request_params.replace("'", '"'))
                if len(request_params) > 0:
                    request_url += '?'
                    for param in request_params:
                        field = param['field']
                        val = param['value']
                        request_url += f'{field}={val}&'
                    request_url = request_url[:-1]


                # PAYLOAD WORK ##########################################
                request_body = post_data['request_body']
                request_body = delimiterReplace(str(request_body), request_payload)
                request_body = json.loads(request_body.replace("'", '"'))

                
                request_method = post_data['request_method']

                req = None
                if request_method == 'GET':
                    req = requests.get(request_url, headers=req_headers)

                if request_method == 'POST':
                    req = requests.post(request_url, json=request_body, headers=req_headers)
                req_data = req.__dict__
                req_data['_content'] = req_data['_content'].decode("utf-8") 
                content = req_data['_content']
                content = content.replace('\n', '')
                req_data.pop('raw')
                req_data.pop('elapsed')
                req_data.pop('connection')
                req_data.pop('request')
                req_data.pop('cookies')
                req_data.pop('_content')
                
                return_data = {}
                return_data['request'] = {}
                return_data['request']['url'] = request_url
                return_data['request']['headers'] = request_headers
                return_data['request']['method'] = request_method
                if request_method == 'POST':
                    return_data['request']['body'] = request_body
                return_data['response'] = {}
                try:
                    return_data['response']['content'] = json.loads(content)
                    return_data['response']['headers'] = req_data['headers']
                    return_data['response']['url'] = req_data['url']
                    return_data['response']['status'] = req_data['status_code']
                except:
                    return_data['response']['error'] = 'Request Failed!'

                return_data = str(return_data)
                return jsonify({'Message':'Success', 'Response':json.loads(return_data.replace("'", '"'))})
    except:
        pass
    return jsonify({'Message':'Failure'})


@campaignsBlueprint.route('/api/v1/campaigns/schedule', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignScheduleAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaignSchedules = mongoDB['campaign_schedule']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('campaignid'):
                    filterBy['campaign_id'] = ObjectId(request.args.get('campaignid'))

                returnPost = []

                for schedule in campaignSchedules.find(filterBy):
                    scheduleData = convertToJSON(schedule)
                    returnPost.append(scheduleData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        else:
            returnPost = simpleUpdateRow(campaignSchedules, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            #client.close()
            return jsonify(returnPost)

def delimiterReplace(str_full, data):
    curr_first = -1
    indices = []
    for indx, char in enumerate(str_full):
        if char == '[':
            curr_first = indx
        elif char == ']' and curr_first != -1:
            indices.append([curr_first, indx])
            curr_first = -1

    first_index = indices[0][0]
    first_part = str_full[0:first_index]
    full_str = first_part
    last_index = 0
    for indx, indice in enumerate(indices):
        first_index = indice[0]
        last_index = indice[1]
        mid_part = str_full[first_index+1:last_index]
        last_index
        try:
            value = data[mid_part]
        except:
            value = str_full[first_index:last_index+1]
        try:
            next_part = str_full[last_index+1:indices[indx+1][0]]
        except:
            next_part = ''
        full_str += value+next_part

    last_part = str_full[last_index+1:len(str_full)]
    full_str += last_part
    return full_str