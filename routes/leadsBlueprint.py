from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *

import requests
from requests.auth import HTTPBasicAuth as ReqHTTPBasicAuth

leadsBlueprint = Blueprint('leadsAPI', __name__)

@leadsBlueprint.route('/api/v1/leads', methods=['GET', 'POST', 'PUT', 'DELETE'])
def leadsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        if request.method == 'GET':
            try:
                filterBy = {}
                twilio_account_sid = ''
                twilio_auth_token = ''
                if request.args.get('leadid'):
                    filterBy['_id'] = ObjectId(request.args.get('leadid'))
                    campaign_col = mongoDB['campaigns']
                    campaign = campaign_col.find_one({'_id':ObjectId(request.args.get('campaignid'))})

                    company_col = mongoDB['companies']
                    company = company_col.find_one({'_id':campaign['company_id']})
                    twilio_account_sid = company['twilio_account_sid']
                    twilio_auth_token = company['twilio_auth_token']

                campaignList = []
                if request.args.get('campaignid') and request.args.get('campaignid') != '':
                    try:
                        filterBy['campaign_id'] = ObjectId(request.args.get('campaignid'))
                    except:
                        pass
                else:
                    try:
                        campaigns = mongoDB['campaigns']
                        for campaign in campaigns.find({'company_id':ObjectId(session['user']['company_id'])}):
                            campaignList.append(campaign['_id'])
                    except:
                        return jsonify({'Message':'Failure'})
                
                
                if request.args.get('from') and request.args.get('to'):
                    filterBy['call_logs.created_at'] = {
                        '$gte' : request.args.get('from'),
                        '$lte' : request.args.get('to'),
                    }

                if request.args.get('status'):
                    filterBy['status'] = request.args.get('status')

                if request.args.get('dnc') == '1':
                    filterBy['dnc'] = True

                if request.args.get('interested') == '1':
                    filterBy['interested'] = 'interested'
                elif request.args.get('interested') == '0':
                    filterBy['interested'] = None
                
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
                leads = None
                max_length = 0
                if len(campaignList) > 0:
                    leads_col = mongoDB['leads']
                    filterBy['campaign_id'] = {'$in':campaignList}
                    print(filterBy)
                    leads = leads_col.find(filterBy).skip(skip).limit(limit).sort("updated_at", pymongo.DESCENDING)
                    max_length = leads_col.count_documents(filterBy)
                else:
                    leads_col = mongoDB['leads']
                    print(filterBy)
                    leads = leads_col.find(filterBy).skip(skip).limit(limit).sort("updated_at", pymongo.DESCENDING)
                    max_length = leads_col.count_documents(filterBy)
                returnPost = []
                
                campaignList = {}
                for lead in leads:
                    leadData = convertToJSON(lead)
                    leadData['max_documents'] = max_length
                    leadData['Email'] = None
                    leadData['First_Name'] = None
                    leadData['Last_Name'] = None
                    leadData['Phone_No'] = None
                    leadData['agent_first_name'] = None
                    leadData['agent_last_name'] = None
                    if request.args.get('callid'):
                        leadData['call_log'] = {}
                    x = 0
                    if request.args.get('leadid'):
                        for call_log in leadData['call_logs']:
                            try:
                                try:
                                    url = 'https://api.twilio.com/2010-04-01/Accounts/{}/Calls/{}/Events.json'.format(twilio_account_sid, call_log['call_id'])
                                    req_call = requests.get(url, auth=ReqHTTPBasicAuth(twilio_account_sid, twilio_auth_token))
                                    req_call_json = req_call.json()
                                    transcriptions = []
                                    transcribe = False
                                    for event in req_call_json['events']:
                                        try:
                                            transcriptions.append('<b>Customer:</b> '+ event['request']['parameters']['speech_result'])
                                            transcribe = True
                                        except:
                                            try:
                                                if event['request']['method'] == 'GET':
                                                    transcriptions.append('<b>AI:</b> '+ str(event['request']['url'])[str(event['request']['url']).rfind('/')+1:-3])
                                                    transcribe = True
                                                #start = str(event['response']['response_body']).index('<Play>')+6
                                                #end = str(event['response']['response_body']).index('</Play>')
                                                #transcriptions.append('<b>AI:</b> '+ str(event['response']['response_body'])[start:end])
                                                #transcribe = True
                                            except:
                                                pass
                                    if transcribe:
                                        leadData['call_logs'][x]['transcription'] = transcriptions
                                        if request.args.get('callid'):
                                            leadData['call_log'] = call_log
                                except:
                                    pass
                                x += 1
                            except:
                                pass

                    returnPost.append(leadData)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                phoneNames = ['Phone','phone','Phone Number','phone number','Phone No.','phone no.','Phone No','phone no','cell phone number','Cell Phone Number','contact number','Contact Number','Contact No.','Mobile','mobile','Mobile No',' mobile no','Mobile Number','mobile number','Customer Number','customer number','Customer number','customer Number', 'Telephone No', 'Telephone', 'telephone no', 'telephone', 'Telephone Number' , 'telephone number']
                zipNames = ['zip', 'zip code', 'postal', 'postal code']
                leads = request.json
                unique_leads = []
                unique_phones = []
                for lead in leads:
                    for lead_data in lead['lead_data']:
                        if str(lead_data['field_name']) in phoneNames:
                            if str(lead_data['field_value']) not in unique_phones:
                                unique_phones.append(str(lead_data['field_value']))
                                unique_leads.append(lead)
                leads = unique_leads
                campaign_id = ObjectId(leads[0]['campaign_id'])
                existingList = []
                goodList = []
                index = 0
                for row in leads_col.find({'campaign_id':campaign_id}):
                    for lead_data in row['lead_data']:
                        try:
                            if str(lead_data['field_name']) in phoneNames:
                                existingList.append(str(lead_data['field_value']))
                        except:
                            pass

                created_at = str(datetime.datetime.utcnow())[:-7]
                postal_codes_col = mongoDB['postal_codes']
                area_codes_col = mongoDB['area_codes']
                will_insert = False
                for data in leads:
                    data['campaign_id'] = campaign_id
                    refNum = data['reference_number']
                    leads[index]['created_at'] = created_at
                    leads[index]['updated_at'] = created_at
                    leads[index]['call_logs'] = []
                    leads[index]['call_recordings'] = []
                    post_found = False
                    for lead_data in data['lead_data']:
                        if str(lead_data['field_name']) in phoneNames:
                            refNum = ''.join(filter(str.isdigit, lead_data['field_value']))
                            if str(refNum) not in existingList:
                                if len(refNum) == 10:
                                    refNum = '+1'+refNum
                                leads[index]['reference_number'] = str(refNum)
                                goodList.append(data)
                                will_insert = True
                        elif str(lead_data['field_name']) in zipNames:
                            try:
                                search_query = {
                                    "zip":str(lead_data['field_value'])[0:5]
                                }
                                postal = postal_codes_col.find_one(search_query)
                                leads[index]['offset'] = getDecimal(postal['offset'])
                                post_found = True
                            except:
                                pass
                    if post_found == False:
                        for lead_data in data['lead_data']:
                            if str(lead_data['field_name']) in phoneNames:
                                refNum = ''.join(filter(str.isdigit, lead_data['field_value']))
                                area_code = ''
                                if len(refNum) == 10:
                                    area_code = refNum[:3]
                                try:
                                    search_query = {
                                        "area":area_code
                                    }
                                    postal = area_codes_col.find_one(search_query)
                                    leads[index]['offset'] = getDecimal(postal['offset'])
                                    post_found = True
                                except:
                                    pass
                                
                    index+=1
                try: 
                    leads_col.insert_many(goodList)
                    #client.close()
                except:
                    pass
                if will_insert:
                    return jsonify({'Message':'Success'})
                return jsonify({'Message':'Failure', 'Error':'No Phone Numbers To Import (Can Be Caused By Duplicate Numbers)'})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            try:
                deleteData = request.json
                lead_id = simpleUpdateRow(leads_col, deleteData, 'DELETE', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                print(lead_id)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@leadsBlueprint.route('/leads/generator/<token>', methods=['POST'])
def leadGenerator(token):
    try:
        referrer = request.origin
        logger.debug(f'Referrer: {referrer}')
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaigns_col = mongoDB['campaigns']
        campaign = campaigns_col.find_one({'_id':ObjectId(token)})
        form_col = mongoDB['forms']
        form = form_col.find_one({'_id':campaign['form_id']})
        if referrer == campaign['white_url']:
            created_at = str(datetime.datetime.utcnow())[:-7]
            new_lead = {
                "reference_number":None,
                "status":"unactioned",
                "interested":None,
                "appointment_booked":"0",
                "campaign_id":ObjectId(token),
                "email_template_id":None,
                "first_actioned_by":None,
                "last_actioned_by":None,
                "time_taken":None,
                "lead_data":[],
                "call_logs":[],
                "created_at":created_at,
                "updated_at":created_at
            }
            phoneNames = ['Phone','phone','Phone Number','phone number','Phone No.','phone no.','Phone No','phone no','cell phone number','Cell Phone Number','contact number','Contact Number','Contact No.','Mobile','mobile','Mobile No',' mobile no','Mobile Number','mobile number','Customer Number','customer number','Customer number','customer Number', 'Telephone No', 'Telephone', 'telephone no', 'telephone', 'Telephone Number' , 'telephone number']
            zipNames = ['zip', 'zip code', 'postal', 'postal code']

            refNum = ''
            postData = None
            if form['webhook_type'] == 'JSON':
                postData = request.json
            else:
                postData = {}
                for key in request.form:
                    postData[key] = request.form.get(key)

            postal_codes_col = mongoDB['postal_codes']
            area_codes_col = mongoDB['area_codes']
            post_found = False

            for field in form['fields']:
                if field['field_name'] in phoneNames:
                    refNum = ''.join(filter(str.isdigit, postData[field['webhook_field']]))
                    if len(refNum) == 10:
                        refNum = '+1'+refNum
                    new_lead['reference_number'] = refNum
                elif str(field['field_name']) in zipNames:
                    try:
                        search_query = {
                            "zip":str(postData[field['webhook_field']])[0:5]
                        }
                        postal = postal_codes_col.find_one(search_query)
                        new_lead['offset'] = getDecimal(postal['offset'])
                        post_found = True
                    except:
                        pass
                try:
                    new_lead['lead_data'].append({
                        'field_name':field['field_name'],
                        'field_value':postData[field['webhook_field']]
                    })
                except:
                    pass
            if post_found == False:
                for field in form['fields']:
                    if field['field_name'] in phoneNames:
                        refNum = ''.join(filter(str.isdigit, postData[field['webhook_field']]))
                        area_code = ''
                        if len(refNum) == 10:
                            area_code = refNum[:3]
                        try:
                            search_query = {
                                "area":area_code
                            }
                            postal = area_codes_col.find_one(search_query)
                            new_lead['offset'] = getDecimal(postal['offset'])
                            post_found = True
                        except:
                            pass
            if new_lead['reference_number'] != None:
                lead_col = mongoDB['leads']
                search_query = {
                    'reference_number':new_lead['reference_number'],
                    'campaign_id':ObjectId(token)
                }
                if not lead_col.find_one(search_query):
                    lead_id = simpleUpdateRow(lead_col, new_lead, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                    new_lead = lead_col.find_one({'_id':ObjectId(lead_id['id'])})
                    returnPost = {
                        'message':'success',
                        'data':convertToJSON(new_lead)
                    }
                    #client.close()
                    return jsonify(returnPost)
                else:
                    #client.close()
                    return jsonify({'Message':'Lead Already Exists'})
            #client.close()
            return jsonify({'Message':'Phone number is required'})
        else:
            return jsonify({'Message':'URL is not whitelisted'})
    except:
        #client.close()
        return jsonify({'Message':'Failure'})

@leadsBlueprint.route('/api/v1/leads/summary', methods=['GET', 'POST', 'PUT', 'DELETE'])
def leadSummaryAPI():
    if validateLogin():
        if request.method == 'GET':
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            try:
                summary = {}
                summary['dispositions'] = []
                leads = None

                total_dict = {}
                time_taken_dict = {}
                interested_dict = {}

                if request.args.get('campaignid'):
                    total_dict = {"$cond": [ {  "$in": [ "$campaign_id", [ObjectId(request.args.get('campaignid'))] ] } , 1, 0 ]}
                    time_taken_dict = {"$cond": [ {  "$in": [ "$campaign_id", [ObjectId(request.args.get('campaignid'))] ] } , "$time_taken", 0 ]}
                    interested_dict = {"$cond": [ { "$and": [ { "$eq": [ "$interested", "interested" ] }, { "$in": [ "$campaign_id", [ObjectId(request.args.get('campaignid'))] ] } ] } , 1, 0 ]}
                    

                else:
                    campaign_list = []
                    filterBy = {
                        "company_id":ObjectId(session['user']['company_id'])
                    }
                    campaigns_col = mongoDB['campaigns']
                    for campaign in campaigns_col.find(filterBy):
                        campaign_list.append(ObjectId(campaign['_id']))         
                    total_dict = {"$cond": [ {  "$in": [ "$campaign_id", campaign_list ] } , 1, 0 ]}
                    time_taken_dict = {"$cond": [ {  "$in": [ "$campaign_id", campaign_list ] } , "$time_taken", 0 ]}
                    interested_dict = {"$cond": [ { "$and": [ { "$eq": [ "$interested", "interested" ] }, { "$in": [ "$campaign_id", campaign_list ] } ] } , 1, 0 ]}
                    

                pipeline = [    
                    { 
                        "$group": { 
                            "_id": '$status',
                            "total":{
                                "$sum": total_dict
                            },
                            "time_taken":{
                                "$sum": time_taken_dict
                            },
                            "interested":{
                                "$sum": interested_dict
                            }
                        }  
                    },
                    {
                        "$project": {
                            "total": "$total",
                            "time_taken": "$time_taken",
                            "interested": "$interested"
                        }
                    }
                ]
                
                leads_col = mongoDB['leads']
                lead_aggr = leads_col.aggregate(pipeline)
                for lead in lead_aggr:
                    summary['dispositions'].append({
                        'name':lead['_id'],
                        'total':lead['total'],
                        'duration':lead['time_taken']
                    })
                
                summary['dispositions'] = sorted(summary['dispositions'], key = lambda i: (i['name'], i['name']))
                #client.close()
                return jsonify(summary)
            except:
                return jsonify({'Message':'Failure'})

@leadsBlueprint.route('/api/v1/leads/counts')
def leadCountsAPI():
    if validateLogin():
        try:
            filterBy = {'status':'started'}
            companyID = ''
            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    companyID = request.args.get('companyid')
                    
            try:
                if session['user']['company_id']:
                    filterBy['company_id'] = session['user']['company_id']
                    companyID = session['user']['company_id']
            except:
                pass

            if request.args.get('campaignid'):
                filterBy['campaign_id'] = request.args.get('campaignid')
            
            limit = 10
            if request.args.get('limit'):
                try:
                    limit = int(request.args.get('limit'))
                except:
                    pass
            leads = []
            
            filterBy = {
                "company_id":ObjectId(session['user']['company_id'])
            }
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            campaigns_col = mongoDB['campaigns']
            campaign_list = []
            for campaign in campaigns_col.find(filterBy):
                campaign_list.append(ObjectId(campaign['_id']))  
            
            if request.args.get('from') and request.args.get('to'):
                fromDate = request.args.get('from') + ' 00:00:00'
                toDate = request.args.get('to') + ' 23:59:59'

            else:
                fromDate = '2021-01-01'
                toDate = '2026-01-01'

            pipeline = [
                {
                    "$match":{
                        "updated_at":{
                            "$gte":fromDate,
                            "$lte":toDate
                        }
                    }
                },
                { 
                    "$group": { 
                        "_id": {
                            "month": { 
                                "$month": {
                                    "$dateFromString":{
                                        "dateString":"$updated_at",
                                        "format": "%Y-%m-%d %H:%M:%S"
                                    }
                                }
                            },
                            "day": { 
                                "$dayOfMonth": {
                                    "$dateFromString":{
                                        "dateString":"$updated_at",
                                        "format": "%Y-%m-%d %H:%M:%S"
                                    }
                                }
                            },
                            "year": { 
                                "$year": {
                                    "$dateFromString":{
                                        "dateString":"$updated_at",
                                        "format": "%Y-%m-%d %H:%M:%S"
                                    }
                                } 
                            }
                        },
                        "total_leads":{
                            "$sum":{
                                "$cond":[
                                    {
                                        "$and":[
                                        {
                                            "$ne":["$status","unactioned"]
                                        },
                                        {
                                            "$in":["$campaign_id",campaign_list]
                                        }
                                        ]
                                    },
                                    1,0]
                            }
                        }
                    }  
                },
                {
                    "$project": {
                        "total_leads": "$total_leads"
                    }
                },{"$sort":{"_id":1}}
            ]
            print(campaign_list)

            returnPost = []
            leads_col = mongoDB['leads']
            leads_agg_result = leads_col.aggregate(pipeline)
            for d in leads_agg_result:
                returnPost.append({
                    'date':'{}/{}/{}'.format(d['_id']['month'], d['_id']['day'], d['_id']['year']),
                    'full_date':'{}-{}-{}'.format(d['_id']['year'], d['_id']['month'], d['_id']['day']),
                    'count':d['total_leads'],
                    'company_id':companyID
                })
            if len(returnPost) == 1:
                returnPost.append(returnPost[0])
            
            #client.close()
            return jsonify(returnPost)
        except:
            return jsonify({'Message':'Failure'})

@leadsBlueprint.route('/api/v1/leads/export')
def leadExportAPI():
    if validateLogin():
        try:
            filterBy = {}
            if request.args.get('campaignid'):
                filterBy['campaign_id'] = ObjectId(request.args.get('campaignid'))
            
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads = mongoDB['leads']

            returnPost = []
            for lead in leads.find(filterBy):
                if lead['lead_data']:
                    newPost = []
                    for x in lead['lead_data']:
                        newPost.append(x['field_value'])
                    returnPost.append(newPost)

            #client.close()
            return jsonify(returnPost)
        except:
            return jsonify({'Message':'Failure'})

@leadsBlueprint.route('/api/v1/leads/recycle', methods=['POST'])
def leadRecycleAPI():
    if validateLogin(): 
        try:   
            post_json = request.json

            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads_col = mongoDB['leads']

            search_query = {}
            search_query['campaign_id'] = ObjectId(post_json['campaign_id'])
            search_query['status'] = {
                '$in':post_json['dispos']
            }
            
            update_query = {
                '$set':{
                    'status':'unactioned'
                }
            }
            leads_col.update_many(search_query, update_query)
            return jsonify({'Message':'Success'})
        except:
            return jsonify({'Message':'Failure'})

@leadsBlueprint.route('/api/v1/leads/time_summary')
def leadTimeSummaryAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_time_summary_col = mongoDB['leads_time_summary']
        companies_col = mongoDB['companies']
        try:
            campaign_ids = []

            company_filter_by = {}
            if request.args.get('companyid'):
                campaigns_col = mongoDB['campaigns']
                filterBy = {
                    'company_id':ObjectId(request.args.get('companyid'))
                }
                company_filter_by = {
                    '_id':ObjectId(request.args.get('companyid'))
                }
                for campaign in campaigns_col.find(filterBy):
                    campaign_ids.append(campaign['_id'])

            company = companies_col.find_one(company_filter_by)
            company_charge_rate = company['billing']['charge_amount']

            from_date = "2022-01-01"
            to_date = "2122-01-01"
            if request.args.get('from'):
                from_date = request.args.get('from')
            if request.args.get('to'):
                to_date = request.args.get('to')
            filterBy = {
                "entry_date":{
                    "$gte":from_date,
                    "$lt":to_date
                }
            }
            filterBy['campaign_id'] = {
                "$in" : campaign_ids
            }
            return_post = {
                'total_time_taken':0,
                'total_time_rounded_taken':0,
                'total_by_date':{},
                'company_id':request.args.get('companyid'),
                'breakdown':[]
            }
            for lead in leads_time_summary_col.find(filterBy):
                return_post['total_time_taken'] += lead['time_taken']
                return_post['total_time_rounded_taken'] += lead['time_taken_rounded']

                if not return_post['total_by_date'].get(lead['entry_date']):
                    return_post['total_by_date'][lead['entry_date']] = {
                        'time_taken_rounded':lead['time_taken_rounded'],
                        'time_taken':lead['time_taken']
                    }
                else:
                    return_post['total_by_date'][lead['entry_date']]['time_taken'] += lead['time_taken']

                return_post['breakdown'].append({
                    'entry_date':lead['entry_date'],
                    'campaign_id':str(lead['campaign_id']),
                    'time_taken':lead['time_taken'],
                    'time_taken_rounded':lead['time_taken_rounded'],
                })
            return_post['total_charge'] = getDecimal(getDecimal(company_charge_rate)*getDecimal(return_post['total_time_rounded_taken']))
            return jsonify(return_post)
        except:
            return jsonify({"Message":"Failure"})

@leadsBlueprint.route('/api/v1/lead/campaign-summary')
def leadCampaignSummaryTestAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        filterBy = {}
            
        try:
            if session['user']['company_id']:
                filterBy['company_id'] = ObjectId(session['user']['company_id'])
            else:
                return jsonify({'Message':'Failure'})
        except:
            return jsonify({'Message':'Failure'})
        
        campaigns_col = mongoDB['campaigns']
        campaign_list = []
        
        for campaign in campaigns_col.find(filterBy):
            campaign_list.append(campaign['_id'])
        
        if request.args.get('campaignid'):
            if ObjectId(request.args.get('campaignid')) in campaign_list:
                filterBy = {
                    "campaign_id": ObjectId(request.args.get('campaignid'))
                }
        else:
            filterBy = {
                "campaign_id": {
                    "$in":campaign_list
                }
            }
        summary_col_old = mongoDB['leads_campaign_summary_new']
        leads_col = mongoDB['leads']

        total_leads = leads_col.count_documents(filterBy)
        total_unactioned = leads_col.count_documents(filterBy)
        returnPost = {
            "calls_made": 0, 
            "call_time": 0, 
            "time_taken": 0, 
            "total_connected": 0, 
            "total_interested": 0, 
            "total_leads": total_leads, 
            "total_unactioned": total_unactioned,
            "campaign_count":len(campaign_list)
        }
        
        if request.args.get('from') and request.args.get('to'):
            filterBy['updated_at'] = {
                '$gte':request.args.get('from'),
                '$lte':request.args.get('to')
            }
        
        pipeline = campaign_summary_pipeline(filterBy)
        for row in leads_col.aggregate(pipeline):
            print(row)
            returnPost["calls_made"] += row["calls_made"]
            returnPost["call_time"] += row["call_time"]
            returnPost["time_taken"] += row["time_taken"]
            returnPost["total_connected"] += row["total_connected"]
            returnPost["total_interested"] += row["total_interested"]

        #client.close()
        return jsonify(returnPost)

@leadsBlueprint.route('/api/v1/lead/campaign-summary-test')
def leadCampaignSummaryAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        filterBy = {}
            
        try:
            if session['user']['company_id']:
                filterBy['company_id'] = ObjectId(session['user']['company_id'])
            else:
                return jsonify({'Message':'Failure'})
        except:
            return jsonify({'Message':'Failure'})
        
        campaigns_col = mongoDB['campaigns']
        campaign_list = []
        
        for campaign in campaigns_col.find(filterBy):
            campaign_list.append(campaign['_id'])
        
        if request.args.get('campaignid'):
            if ObjectId(request.args.get('campaignid')) in campaign_list:
                filterBy = {
                    "campaign_id": ObjectId(request.args.get('campaignid'))
                }
        else:
            filterBy = {
                "campaign_id": {
                    "$in":campaign_list
                }
            }
        
        if request.args.get('from') and request.args.get('to'):
            filterBy['updated_at'] = {
                '$gte':request.args.get('from'),
                '$lte':request.args.get('to')
            }
        
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        data = leads_col.find(filterBy)
        df = pd.DataFrame(data=data)
        df['updated_at_formatted'] = pd.to_datetime(df['updated_at']).dt.date
        df_total_seconds = df.groupby([df['updated_at_formatted'], 'status', 'campaign_id']).count()
        dict_obj = df_total_seconds.to_dict()
        del df_total_seconds
        del df
        return_post = {
            'totals':{
                'details':{},
                'totals':{}
            },
            'campaign_totals':{},
            'summary':{
                "call_time":0,
                "calls_made":0,
                "campaign_count":0,
                "time_taken":0,
                "total_connected":0,
                "total_interested":0,
                "total_leads":0,
                "total_unactioned":0
            }
        }
        for row in dict_obj:
            if row == '_id':
                for x in dict_obj[row]:
                    entry_date = str(x[0])
                    status = str(x[1])
                    if not return_post['totals']['details'].get(entry_date):
                        return_post['totals']['details'][entry_date] = {}
                    if not return_post['totals']['details'][entry_date].get(status):
                        return_post['totals']['details'][entry_date][status] = 0
                    return_post['totals']['details'][entry_date][status] += dict_obj[row][x]

                    if not return_post['totals']['totals'].get(status):
                        return_post['totals']['totals'][status] = 0
                    return_post['totals']['totals'][status] += dict_obj[row][x]

                    if status == 'unactioned':
                        return_post['summary']['total_unactioned'] += dict_obj[row][x]

        for row in dict_obj:
            if row == '_id':
                for x in dict_obj[row]:
                    campaign_id = str(x[2])
                    entry_date = str(x[0])
                    status = str(x[1])
                    if not return_post['campaign_totals'].get(campaign_id):
                        return_post['campaign_totals'][campaign_id] = {}
                    if not return_post['campaign_totals'][campaign_id].get(entry_date):
                        return_post['campaign_totals'][campaign_id][entry_date] = {}
                    if not return_post['campaign_totals'][campaign_id][entry_date].get(status):
                        return_post['campaign_totals'][campaign_id][entry_date][status] = 0
                    return_post['campaign_totals'][campaign_id][entry_date][status] += dict_obj[row][x]
        try:
            filterBy.pop('updated_at')
        except:
            pass   
        data = leads_col.find(filterBy)
        df = pd.DataFrame(data=data)
        df_totals = df.groupby(['status']).count()
        df_totals_dict = df_totals.to_dict()
        del df_totals
        del df
        for row in df_totals_dict:
            if row == '_id':
                print({
                    row:df_totals_dict[row]
                })
            break
        return jsonify(return_post)
