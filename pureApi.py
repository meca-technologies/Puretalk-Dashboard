from operator import pos
from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from flask_httpauth import HTTPBasicAuth
from app import session, app
from aggrFunctions import *
import datetime
import time
import pytz
from dateutil.relativedelta import relativedelta
import pymongo

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from werkzeug.utils import redirect

import bcrypt

apiBlueprint = Blueprint('pureAPI', __name__)

import requests
from requests.auth import HTTPBasicAuth as ReqHTTPBasicAuth

import config
from pyAreadCodes import areaCodeTZ
from pyStateLaws import stateLaws
import pyAreadCodes
import pyPostalCodes

import string
import os
import math
from bson.objectid import ObjectId

import stripe

from app import logger
from vicidialAPI import getGMTOffset

import pymysql.cursors
from sqlescapy import sqlescape

import numpy as np
import pandas as pd

from univFuncs import *

auth = HTTPBasicAuth()

@apiBlueprint.route('/api/v1/validate-login', methods=['GET'])
def apiValidateLogin():
    if validateLogin():
        return jsonify({'Message':"Success"})
    return jsonify({'Message':"Failure"})

@apiBlueprint.route('/set-company-id')
def setCompanyID():
    if validateLogin():
        if request.args.get('companyid') and request.args.get('call_type'):
            companyID = request.args.get('companyid')
            if validateCompany(companyID):
                session['user']['company_id'] = companyID
                #company = Companies.query.filter_by(id=companyID).first()
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                companies_col = mongoDB['companies']
                company = companies_col.find_one({"_id":ObjectId(companyID)})
                session['company'] = {
                    'id':companyID,
                    'logo':company['logo'],
                    'package_type':company['package_type'],
                    'name':company['name'],
                    'email':company['email'],
                    'phone':company['phone'],
                    'website':company['website'],
                    'address':company['address'],
                    'app_layout':company['app_layout'],
                    'rtl':company['rtl'],
                    'status':company['status']
                }
                session['call_type'] =  request.args.get('call_type')
                if session['user']['super_admin'] == True:
                    session['permission_sets'] = {
                        companyID:{
                            "613b89ed3e1f2f627b4892f2":{
                                "display_name":"Staff Create",
                                "id":"613b89ed3e1f2f627b4892f2",
                                "name":"staff_create"
                            },
                            "613b89ed3e1f2f627b4892f3":{
                                "display_name":"Staff Edit",
                                "id":"613b89ed3e1f2f627b4892f3",
                                "name":"staff_edit"
                            },
                            "613b89ed3e1f2f627b4892f4":{
                                "display_name":"Staff Delete",
                                "id":"613b89ed3e1f2f627b4892f4",
                                "name":"staff_delete"
                            },
                            "613b89ed3e1f2f627b4892f5":{
                                "display_name":"Staff Assign Role",
                                "id":"613b89ed3e1f2f627b4892f5",
                                "name":"assign_role"
                            },
                            "613b89ed3e1f2f627b4892f6":{
                                "display_name":"Sales Member Create",
                                "id":"613b89ed3e1f2f627b4892f6",
                                "name":"sales_member_create"
                            },
                            "613b89ed3e1f2f627b4892f7":{
                                "display_name":"Sales Member Edit",
                                "id":"613b89ed3e1f2f627b4892f7",
                                "name":"sales_member_edit"
                            },
                            "613b89ed3e1f2f627b4892f8":{
                                "display_name":"Sales Member Delete",
                                "id":"613b89ed3e1f2f627b4892f8",
                                "name":"sales_member_delete"
                            },
                            "613b89ed3e1f2f627b4892f9":{
                                "display_name":"Import Lead",
                                "id":"613b89ed3e1f2f627b4892f9",
                                "name":"import_lead"
                            },
                            "613b89ed3e1f2f627b4892fa":{
                                "display_name":"Export Lead",
                                "id":"613b89ed3e1f2f627b4892fa",
                                "name":"export_lead"
                            },
                            "613b89ed3e1f2f627b4892fb":{
                                "display_name":"View Campaigns",
                                "id":"613b89ed3e1f2f627b4892fb",
                                "name":"campaign_view"
                            },
                            "613b89ed3e1f2f627b4892fc":{
                                "display_name":"View All Campaigns",
                                "id":"613b89ed3e1f2f627b4892fc",
                                "name":"campaign_view_all"
                            },
                            "613b89ed3e1f2f627b4892fd":{
                                "display_name":"Campaign Create",
                                "id":"613b89ed3e1f2f627b4892fd",
                                "name":"campaign_create"
                            },
                            "613b89ed3e1f2f627b4892fe":{
                                "display_name":"Campaign Edit",
                                "id":"613b89ed3e1f2f627b4892fe",
                                "name":"campaign_edit"
                            },
                            "613b89ed3e1f2f627b4892ff":{
                                "display_name":"Campaign Delete",
                                "id":"613b89ed3e1f2f627b4892ff",
                                "name":"campaign_delete"
                            },
                            "613b89ed3e1f2f627b489300":{
                                "display_name":"View Email Template",
                                "id":"613b89ed3e1f2f627b489300",
                                "name":"email_template_view"
                            },
                            "613b89ed3e1f2f627b489301":{
                                "display_name":"View All Email Templates",
                                "id":"613b89ed3e1f2f627b489301",
                                "name":"email_template_view_all"
                            },
                            "613b89ed3e1f2f627b489302":{
                                "display_name":"Email Template Create",
                                "id":"613b89ed3e1f2f627b489302",
                                "name":"email_template_create"
                            },
                            "613b89ed3e1f2f627b489303":{
                                "display_name":"Email Template Edit",
                                "id":"613b89ed3e1f2f627b489303",
                                "name":"email_template_edit"
                            },
                            "613b89ed3e1f2f627b489304":{
                                "display_name":"Email Template Delete",
                                "id":"613b89ed3e1f2f627b489304",
                                "name":"email_template_delete"
                            },
                            "613b89ed3e1f2f627b489305":{
                                "display_name":"View Campaign Forms",
                                "id":"613b89ed3e1f2f627b489305",
                                "name":"form_view"
                            },
                            "613b89ed3e1f2f627b489306":{
                                "display_name":"View All Campaign Forms",
                                "id":"613b89ed3e1f2f627b489306",
                                "name":"form_view_all"
                            },
                            "613b89ed3e1f2f627b489307":{
                                "display_name":"Form Campaign Create",
                                "id":"613b89ed3e1f2f627b489307",
                                "name":"form_create"
                            },
                            "613b89ed3e1f2f627b489308":{
                                "display_name":"Form Campaign Edit",
                                "id":"613b89ed3e1f2f627b489308",
                                "name":"form_edit"
                            },
                            "613b89ed3e1f2f627b489309":{
                                "display_name":"Form Campaign Delete",
                                "id":"613b89ed3e1f2f627b489309",
                                "name":"form_delete"
                            },
                            "61575f55679cf939aca4ad74":{
                                "display_name":"AI Agents View",
                                "id":"61575f55679cf939aca4ad74",
                                "name":"ai_agents_view"
                            },
                            "61575f56679cf939aca4ad75":{
                                "display_name":"AI Agents Edit",
                                "id":"61575f56679cf939aca4ad75",
                                "name":"ai_agents_edit"
                            },
                            "61575f56679cf939aca4ad76":{
                                "display_name":"AI Agents Delete",
                                "id":"61575f56679cf939aca4ad76",
                                "name":"ai_agents_delete"
                            },
                            "61575f823c986a2f938bc0be":{
                                "display_name":"Call Manager View",
                                "id":"61575f823c986a2f938bc0be",
                                "name":"call_manager_view"
                            },
                            "61575f833c986a2f938bc0bf":{
                                "display_name":"Call Manager Edit",
                                "id":"61575f833c986a2f938bc0bf",
                                "name":"call_manager_edit"
                            },
                            "61575f843c986a2f938bc0c0":{
                                "display_name":"Call Manager Delete",
                                "id":"61575f843c986a2f938bc0c0",
                                "name":"call_manager_delete"
                            },
                            "61575fb85e41d8e13fea3888":{
                                "display_name":"Call History View",
                                "id":"61575fb85e41d8e13fea3888",
                                "name":"call_history_view"
                            },
                            "61575fb95e41d8e13fea3889":{
                                "display_name":"Call History Edit",
                                "id":"61575fb95e41d8e13fea3889",
                                "name":"call_history_edit"
                            },
                            "61575fb95e41d8e13fea388a":{
                                "display_name":"Call History Delete",
                                "id":"61575fb95e41d8e13fea388a",
                                "name":"call_history_delete"
                            },
                            "6157600411599235efcae347":{
                                "display_name":"Import Caller IDs",
                                "id":"6157600411599235efcae347",
                                "name":"import_caller_ids"
                            },
                            "61576045b38aa96d7e7e566f":{
                                "display_name":"Caller IDs View",
                                "id":"61576045b38aa96d7e7e566f",
                                "name":"caller_id_view"
                            },
                            "61576046b38aa96d7e7e5670":{
                                "display_name":"Caller IDs Edit",
                                "id":"61576046b38aa96d7e7e5670",
                                "name":"caller_id_edit"
                            },
                            "61576046b38aa96d7e7e5671":{
                                "display_name":"caller_id_delete",
                                "id":"61576046b38aa96d7e7e5671",
                                "name":"Caller IDs Delete"
                            },
                            "6157607468e998dff84941a7":{
                                "display_name":"Billing View",
                                "id":"6157607468e998dff84941a7",
                                "name":"billing_view"
                            },
                            "6157607568e998dff84941a8":{
                                "display_name":"Billing Edit",
                                "id":"6157607568e998dff84941a8",
                                "name":"billing_edit"
                            },
                            "6157607568e998dff84941a9":{
                                "display_name":"Billing Delete",
                                "id":"6157607568e998dff84941a9",
                                "name":"billing_delete"
                            },
                            "6157637df5708a04ced1ba68":{
                                "display_name":"Settings View",
                                "id":"6157637df5708a04ced1ba68",
                                "name":"settings_view"
                            },
                            "6157637ef5708a04ced1ba69":{
                                "display_name":"Settings Edit",
                                "id":"6157637ef5708a04ced1ba69",
                                "name":"settings_edit"
                            },
                            "6157637ef5708a04ced1ba6a":{
                                "display_name":"Settings Delete",
                                "id":"6157637ef5708a04ced1ba6a",
                                "name":"settings_delete"
                            },
                            "613b89ed3e1f2f627b4892fb":{
                                "display_name":"View Campaigns",
                                "id":"613b89ed3e1f2f627b4892fb",
                                "name":"campaign_view"
                            },
                            "613b89ed3e1f2f627b4892fc":{
                                "display_name":"View All Campaigns",
                                "id":"613b89ed3e1f2f627b4892fc",
                                "name":"campaign_view_all"
                            },
                            "613b89ed3e1f2f627b489300":{
                                "display_name":"View Email Template",
                                "id":"613b89ed3e1f2f627b489300",
                                "name":"email_template_view"
                            },
                            "613b89ed3e1f2f627b489306":{
                                "display_name":"View All Campaign Forms",
                                "id":"613b89ed3e1f2f627b489306",
                                "name":"form_view_all"
                            },
                            "61575f823c986a2f938bc0be":{
                                "display_name":"Call Manager View",
                                "id":"61575f823c986a2f938bc0be",
                                "name":"call_manager_view"
                            },
                            "61575fb85e41d8e13fea3888":{
                                "display_name":"Call History View",
                                "id":"61575fb85e41d8e13fea3888",
                                "name":"call_history_view"
                            },
                            "61576045b38aa96d7e7e566f":{
                                "display_name":"Caller IDs View",
                                "id":"61576045b38aa96d7e7e566f",
                                "name":"caller_id_view"
                            },
                            "6157607468e998dff84941a7":{
                                "display_name":"Billing View",
                                "id":"6157607468e998dff84941a7",
                                "name":"billing_view"
                            },
                            "618e9207b915bfe19a75e2f2":{
                                "display_name":"Campaign Management",
                                "id":"618e9207b915bfe19a75e2f2",
                                "name":"campaign_management"
                            },
                            "618e922cb915bfe19a75e2f3":{
                                "display_name":"Lead Management",
                                "id":"618e922cb915bfe19a75e2f3",
                                "name":"lead_management"
                            },
                            "618e924bb915bfe19a75e2f4":{
                                "id":"618e924bb915bfe19a75e2f4"
                            }
                        }
                    }
                    
                #client.close()
                return redirect('/')
            try:  
                session['user'].pop('company_id', None)
            except:
                pass
            return redirect('/companies')
    return redirect('/login')

@apiBlueprint.route('/api/bot', methods=['GET', 'POST', 'PUT', 'DELETE'])
def aiAPI():
    return send_file('static/testResponse.xml')

@apiBlueprint.route('/api/v1/ai-agents', methods=['GET', 'POST', 'PUT', 'DELETE'])
def aiAgentsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        aiAgents = mongoDB['ai_agents']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('agentid'):
                    filterBy['id'] = request.args.get('agentid')

                if request.args.get('userid'):
                    filterBy['user_id'] = request.args.get('userid')
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []

                for aiAgent in aiAgents.find():
                    valid = True
                    try:
                        if session['user']['company_id']:
                            users_col = mongoDB['users']
                            aiAgentCompany = users_col.find_one({'id':ObjectId(aiAgent['user_id'])})
                            if str(aiAgentCompany['company_id']) != str(session['user']['company_id']):
                                valid = False
                    except:
                        pass
                    
                    if valid:
                        returnPost.append(convertToJSON(aiAgent))
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            try:
                simpleUpdateRow(aiAgents, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                #client.close()
                return jsonify({'Message':'Success'})
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/virtual-agents', methods=['GET', 'POST', 'PUT', 'DELETE'])
def virtualAgentsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        virtualAgents = mongoDB['virtual_agents']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('agentid'):
                    filterBy['_id'] = ObjectId(request.args.get('agentid'))

                try:
                    if session['user']['company_id']:
                        try:
                            filterBy['company_id'] = ObjectId(session['user']['company_id'])
                        except:
                            pass
                        filterBy['status'] = True
                    else:
                        company_list = []
                        for company in session['companies']:
                            company_list.append(ObjectId(company))
                        filterBy['company_id'] = {
                            "$in" : company_list
                        }
                except:
                    pass
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                
                returnPost = []
                for virtualAgent in virtualAgents.find(filterBy):
                    virtualAgentData = convertToJSON(virtualAgent)
                    try:
                        companies_col = mongoDB['companies']
                        company = companies_col.find_one({'_id':ObjectId(virtualAgentData['company_id'])})
                        virtualAgentData['company_name'] = company['name']
                    except:
                        pass
                    returnPost.append(virtualAgentData)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            #try:
            post_data = request.json
            if request.method == 'POST':
                companies_col = mongoDB['companies']
                company = companies_col.find_one({'_id':ObjectId(post_data['company_id'])})
                twilio_account_sid = company['twilio_account_sid']
                twilio_auth_token = company['twilio_auth_token']
                twilClient = Client(twilio_account_sid, twilio_auth_token)
                application = twilClient.applications \
                .create(
                        voice_method='POST',
                        voice_url=post_data['voice_url'],
                        friendly_name=post_data['name']
                )
                post_data['app_id'] = application.sid
            elif request.method == 'PUT':
                virtual_agent = virtualAgents.find_one({'_id':ObjectId(post_data['id'])})
                if virtual_agent['company_id'] == post_data['company_id']:
                    companies_col = mongoDB['companies']
                    company = companies_col.find_one({'_id':ObjectId(post_data['company_id'])})
                    twilio_account_sid = company['twilio_account_sid']
                    twilio_auth_token = company['twilio_auth_token']
                    twilClient = Client(twilio_account_sid, twilio_auth_token)
                    application = twilClient.applications(post_data['app_id']) \
                    .update(
                        voice_url=post_data['voice_url']
                    )
                else:
                    print('Moving Companies')
                    # SINCE WE ARE SWAPPING COMPANIES WE NEED TO DELETE THE OLD ONE AND CREATE A NEW ONE IN THE OTHER COMPANY
                    companies_col = mongoDB['companies']
                    company = companies_col.find_one({'_id':ObjectId(virtual_agent['company_id'])})
                    twilio_account_sid = company['twilio_account_sid']
                    twilio_auth_token = company['twilio_auth_token']
                    twilClient = Client(twilio_account_sid, twilio_auth_token)
                    twilClient.applications(virtual_agent['app_id']).delete()
                    print('Deleted old one')

                    # CREATE NEW ONE
                    company = companies_col.find_one({'_id':ObjectId(post_data['company_id'])})
                    twilio_account_sid = company['twilio_account_sid']
                    twilio_auth_token = company['twilio_auth_token']
                    twilClient = Client(twilio_account_sid, twilio_auth_token)
                    application = twilClient.applications \
                    .create(
                            voice_method='POST',
                            voice_url=post_data['voice_url'],
                            friendly_name=post_data['name']
                    )
                    post_data['app_id'] = application.sid
                    print('Created new one')
            elif request.method == 'DELETE':
                # DELETE FROM TWILIO
                print('Deleted from Twilio')
                companies_col = mongoDB['companies']
                virtual_agent = virtualAgents.find_one({'_id':ObjectId(post_data['id'])})
                company = companies_col.find_one({'_id':ObjectId(virtual_agent['company_id'])})
                twilio_account_sid = company['twilio_account_sid']
                twilio_auth_token = company['twilio_auth_token']
                twilClient = Client(twilio_account_sid, twilio_auth_token)
                twilClient.applications(virtual_agent['app_id']).delete()

            message = simpleUpdateRow(virtualAgents, post_data, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            #client.close()
            return jsonify({'Message':message['Message']})
            #except:
            #    #client.close()
            #    return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/articles', methods=['GET', 'POST', 'PUT', 'DELETE'])
def articlesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        articles = mongoDB['articles']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('articleid'):
                    filterBy['_id'] = ObjectId(request.args.get('articleid'))
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                
                returnPost = []

                for article in articles.find(filterBy):
                    user_col = mongoDB['users']
                    user = user_col.find_one({'_id':ObjectId(article['user_id'])})
                    articleData = convertToJSON(article)
                    articleData['user_first_name'] = user['first_name']
                    articleData['user_last_name'] = user['last_name']
                    returnPost.append(articleData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
                try:
                    return jsonify(simpleUpdateRow(articles, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(',')))
                except:
                    return jsonify({'Message':'Failure'})
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/appointments', methods=['GET', 'POST', 'PUT', 'DELETE'])
def appointmentsAPI():
    if validateLogin():
        if request.method == 'GET':
            return jsonify({"Message":"Failure"})

@apiBlueprint.route('/api/v1/follow-calls', methods=['GET', 'POST', 'PUT', 'DELETE'])
def followUpCallsAPI():
    if validateLogin():
        if request.method == 'GET':
            return jsonify({"Message":"Failure"})
            
@apiBlueprint.route('/api/v1/companies', methods=['GET', 'POST', 'PUT', 'DELETE'])
def companiesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        companies = mongoDB['companies']
        if request.method == 'GET':
            try:
                company_list = []
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['_id'] = ObjectId(request.args.get('companyid'))
                else:
                    for company in session['companies']:
                        company_list.append(ObjectId(company))
                    filterBy = {
                        "_id":{
                            "$in" : company_list
                        }
                    }
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass

                returnPost = []
                for company in companies.find(filterBy):
                    logoName = '/static/img/brand/default.png'
                    companyData = convertToJSON(company)
                    if company['logo']:
                        logoName = '/static/img/brand/'+str(company['logo'])
                    companyData['logo'] = logoName

                    companyData['total_users'] = 0
                    
                    if request.args.get('companyid'):
                        filterBy = {
                            'company_id':company['_id']
                        }
                        company_billing_col = mongoDB['company_billing']
                        billing = company_billing_col.find_one(filterBy)
                        if billing:
                            companyData['charge_type'] = billing['charge_type']
                            companyData['charge_amount'] = billing['charge_amount']
                        else:
                            companyData['charge_type'] = 0
                            companyData['charge_amount'] = 0.35
                    returnPost.append(companyData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                if postData['create_twilio_sub']:
                    twil_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_SID)

                    account = twil_client.api.accounts.create(friendly_name=postData['name'])
                    postData['twilio_account_sid'] = str(account.sid)
                    postData['twilio_auth_token'] = str(account.auth_token)
                newRow = simpleUpdateRow(companies, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))

                # WE WANT TO ADD THAT COMPANY TO OUR CURRENT LIST AND TO DO THAT WE
                # WILL ADD A NEW ADMIN ROLE AND ASSIGN IT TO US
                if session['companies']:
                    postData = {
                        'company_id':newRow['id'],
                        'name':'Admin',
                        'display_name':'Admin',
                        'description':'Built In Admin Role',
                        'permissions':[]
                    }
                    roles_col = mongoDB['roles']
                    newRoleRow = simpleUpdateRow(roles_col, postData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))

                    postData = {
                        'user_id':session['user']['user_id'],
                        'role_id':newRoleRow['id']
                    }
                    roles_col = mongoDB['role_user_new']
                    newRoleRow = simpleUpdateRow(roles_col, postData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))

                    companiesList = session['companies']
                    companiesList.append(newRow['id'])
                    session['companies'] = companiesList

            except:
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'PUT':
            try:
                updateData = request.json
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                print(updateData)
                simpleUpdateRow(companies, updateData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                try:
                    billing = updateData['billing']
                    #updateData.pop('billing')
                except:
                    billing = None
                if billing:
                    print('Billing')
                    filterBy = {
                        'company_id':ObjectId(billing['company_id'])
                    }
                    company_billing_col = mongoDB['company_billing']
                    updateRow = company_billing_col.find_one(filterBy)
                    if updateRow:
                        print('Update')
                        simpleUpdateRow(company_billing_col, billing, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                    else:
                        print('Insert')
                        simpleUpdateRow(company_billing_col, billing, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'DELETE':
            try:
                returnPost = simpleUpdateRow(companies, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                #client.close()
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify(returnPost)

@apiBlueprint.route('/api/v1/companies/first-time')
def companyFirstTimeAPI():
    try:
        returnPost = {}
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaigns_col = mongoDB['campaigns']
        filterBy = {}
        if session['user']['company_id']:
            filterBy['company_id'] = ObjectId(session['user']['company_id'])
        campaigns = []
        for campaign in campaigns_col.find(filterBy):
            campaignData = convertToJSON(campaign)

            campaignData['leads'] = []

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
            campaigns.append(campaignData)
        returnPost['campaign_length'] = len(campaigns)

        forms = mongoDB['forms']
        filterBy = {}

        try:
            if session['user']['company_id']:
                filterBy['company_id'] = ObjectId(session['user']['company_id'])
        except:
            pass

        if forms.find_one(filterBy):
            returnPost['form_length'] = 1
        else:
            returnPost['form_length'] = 0
        
        leads_col = mongoDB['leads']
        filterBy = {}
        campaignList = []
        try:
            for campaign in campaigns:
                campaignList.append(ObjectId(campaign['id']))
        except:
            return 0
        
        if len(campaignList) > 0:
            filterBy['campaign_id'] = {'$in':campaignList}
            if leads_col.find_one(filterBy):
                returnPost['lead_length'] = 1
            else:
                returnPost['lead_length'] = 0
        else:
            returnPost['lead_length'] = 0
        return jsonify(returnPost)
    except:
        return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/companies/summary')
def companySummaryAPI():
    try:
        if validateLogin():
            #try:
            filterBy = {}

            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    filterBy['company_id'] = ObjectId(request.args.get('companyid'))
            
            try:
                if session['user']['company_id']:
                    filterBy['company_id'] = ObjectId(session['user']['company_id'])
                else:
                    company_list = []
                    for company in company_list:
                        company_list.append(ObjectId(company))
                    filterBy['company_id'] = {
                        '$in':company_list
                    }
            except:
                pass
            
            limit = 10
            if request.args.get('limit'):
                try:
                    limit = int(request.args.get('limit'))
                except:
                    pass

            returnPost = {}
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            campaigns_col = mongoDB['campaigns']
            company_list = []
            
            campaigns_col = mongoDB['campaigns']
            campaign_list = []
            
            for campaign in campaigns_col.find(filterBy):
                campaign_list.append(campaign['_id'])

            companies_col = mongoDB['companies']
            for company in session['companies']:
                company_list.append(ObjectId(company))
            pipeline = []
            company_active_dict = {}
            company_expire_dict = {}

            camp_count_dict = {}
            try:
                if session['user']['company_id']:
                    company_active_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "active" ] }, { "$eq": [ "$_id", session['user']['company_id'] ] } ] } , 1, 0 ]}
                    company_expire_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "license_ex" ] }, { "$eq": [ "$_id", session['user']['company_id'] ] } ] } , 1, 0 ]}

                    camp_count_dict = {"$cond": [ { "$and": [ { "$ne": [ "$status", "completed" ] }, { "$eq": [ "$company_id", session['user']['company_id'] ] } ] } , 1, 0 ]}
                else:
                    company_active_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "active" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}
                    company_expire_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "license_ex" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}

                    camp_count_dict = {"$cond": [ { "$and": [ { "$ne": [ "$status", "completed" ] }, { "$in": [ "$company_id", company_list ] } ] } , 1, 0 ]}
            except:
                company_active_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "active" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}
                company_expire_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "license_ex" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}

                camp_count_dict = {"$cond": [ { "$and": [ { "$ne": [ "$status", "completed" ] }, { "$in": [ "$company_id", company_list ] } ] } , 1, 0 ]}
            
            pipeline = [    
                { 
                    "$group": { 
                        "_id": None,
                        "ActiveCounts":{
                            "$sum": company_active_dict
                        },
                        "ExpireCounts":{
                            "$sum": company_expire_dict
                        }
                    }  
                },
                {
                    "$project": {
                        "ActiveCounts": "$ActiveCounts",
                        "ExpireCounts": "$ExpireCounts"
                    }
                }
            ]
            company_aggr = companies_col.aggregate(pipeline)
            for i in company_aggr:
                returnPost['ActiveCompanyCounts'] = getInt(i['ActiveCounts'])
                returnPost['ExpiredCompanyCounts'] = getInt(i['ExpireCounts'])

            pipeline = [    
                { 
                    "$group": { 
                        "_id": "$_id",
                        "CampCounts":{
                            "$sum": camp_count_dict
                        }
                    }  
                },
                {
                    "$project": {
                        "CampCounts": "$CampCounts"
                    }
                }
            ]
            company_aggr = campaigns_col.aggregate(pipeline)
            for i in company_aggr:
                returnPost['CampaignCount'] = getInt(i['CampCounts'])
            returnPost['CompanyCounts'] = len(company_list)

            

            leadFilterBy = {
                "campaign_id": {
                    "$in":campaign_list
                }
            }
            leads_campaign_summary = mongoDB['leads_campaign_summary']
            LeadCount = 0
            CallsMade = 0
            TotalCallLengthSeconds = 0
            TotalInterested = 0
            for lead in leads_campaign_summary.find(leadFilterBy):
                LeadCount += lead['total_leads']
                CallsMade += lead['calls_made']
                TotalCallLengthSeconds += lead['time_taken']
                TotalInterested += lead['interested']
            returnPost['LeadCount'] = LeadCount
            returnPost['CallsMade'] = CallsMade
            returnPost['TotalCallLengthSeconds'] = TotalCallLengthSeconds
            returnPost['TotalInterested'] = TotalInterested

            returnPost['CampaignCount'] = len(campaign_list)
            returnPost['SubscriptionPlans'] = 2

            #client.close()
            return jsonify(returnPost)
    except:
        return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/company-logo', methods=['POST'])
def companyLogoAPI():
    if validateLogin():
        if request.method == 'POST':
            try:
                isthisFile=request.files.get('file')
            except:
                return jsonify({'Message':'Failure'})
            if isthisFile:
                newName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                fileExtention = str(isthisFile.filename).split('.')[1]
                newFileName = newName + '.' + fileExtention
                
                updateData = {
                    'id':request.form['id'],
                    'logo':newFileName
                }
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                companies_col = mongoDB['companies']
                simpleUpdateRow(companies_col, updateData, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                isthisFile.save(os.path.join(config.brand_path, newFileName))
                #client.close()
                return jsonify({'Message':'Success'})
        return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/email', methods=['GET', 'POST', 'PUT', 'DELETE'])
def emailAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        email_settings = mongoDB['email_settings']
        if request.method == 'GET':
            try:
                filterBy = {}

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass

                returnPost = []

                for email in email_settings.find(filterBy):
                    userData = convertToJSON(email)
                    returnPost.append(userData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

        else:
            try:
                req_method = request.method
                req_json = request.json
                if req_json['id'] == '':
                    req_method = 'POST'
                    req_json['company_id'] = ObjectId(session['user']['company_id'])
                returnPost = simpleUpdateRow(email_settings, req_json, req_method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
    
@apiBlueprint.route('/api/v1/forms', methods=['GET', 'POST', 'PUT', 'DELETE'])
def formsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        forms = mongoDB['forms']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
            
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass

                if request.args.get('formid'):
                    filterBy['_id'] = ObjectId(request.args.get('formid'))
                returnPost = []
                for form in forms.find(filterBy):
                    defaultFields = [
                        {
                            'field_name':'First Name',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Last Name',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Company Name',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Website',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Notes',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Email',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Phone No',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Mobile No',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Telephone No',
                            'field_enabled':False
                        }
                    ]
                    fields = []
                    for field in form['fields']:
                        blankField = {
                            'field_name':field['field_name'],
                            'field_enabled':False
                        }
                        if blankField in defaultFields:
                            index = defaultFields.index(blankField)
                            defaultFields[index]['field_enabled'] = True

                        fields.append(convertToJSON(field))

                    #user_col = mongoDB['users']
                    #user = user_col.find_one({'_id':form['created_by']})
                    ##user = Users.query.filter_by(id=form.created_by).first()
                    form = convertToJSON(form)
                    #form['user_first_name'] = user['first_name']
                    #form['user_last_name'] = user['last_name']
                    #form['fields'] = fields
                    form['default_fields'] = defaultFields
                    returnPost.append(form)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            postData = request.json
            if request.method == 'POST':
                postData['company_id'] = session['user']['company_id']
                postData['fields'] = []
            returnPost = simpleUpdateRow(forms, postData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            #client.close()
            return jsonify(returnPost)

@apiBlueprint.route('/api/v1/global-settings', methods=['GET', 'PUT'])
def globalSettingsAPI():
    if validateLogin():
        try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            global_settings_col = mongoDB['global_settings']
            if request.method == 'GET':
                try:
                    if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
                        global_settings = global_settings_col.find_one()
                        returnPost = {}
                        if global_settings:
                            returnPost = convertToJSON(global_settings)
                            returnPost['logo'] = '/static/img/brand/'+global_settings['logo']
                        #client.close()
                        return jsonify(returnPost)
                    return jsonify({'Message':'Failure'})
                except:
                    #client.close()
                    return jsonify({'Message':'Failure'})
            else:
                try:
                    data = request.json
                    returnPost = simpleUpdateRow(global_settings_col, data, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                    #client.close()
                    return jsonify(returnPost)
                except:
                    #client.close()
                    return jsonify({'Message':'Failure'})
        except:
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/unkown_intents', methods=['GET', 'PUT'])
def unkownIntentsAPI():
    try:
        if validateLogin():
            if request.method == 'GET':
                filterBy = {
                    "company_id":ObjectId(session['user']['company_id'])
                }
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                campaigns_col = mongoDB['campaigns']
                campaign_list = []
                for campaign in campaigns_col.find(filterBy):
                    campaign_list.append(str(campaign['_id'])) 

                filterBy = {
                    'checked':False
                }
                passed_check = False
                if request.args.get('campaignid'):
                    if request.args.get('campaignid') in campaign_list:
                        filterBy['campaign_id'] = ObjectId(request.args.get('campaignid'))
                        passed_check = True
                if passed_check:
                    unknown_intents_col = mongoDB['unknown_intents']
                    unknown_intents = unknown_intents_col.find(filterBy)
                    return_post = []
                    for row in unknown_intents:
                        return_post.append(convertToJSON(row))
                    return jsonify(return_post)
            elif request.method == 'PUT':
                updateData = request.json
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                mongoDB = app.mongo_client['jamesbon']
                unknown_intents_col = mongoDB['unknown_intents']
                simpleUpdateRow(unknown_intents_col, updateData, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                return jsonify({'Message':'Success'})
    except:
        pass
    return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/roles', methods=['GET', 'POST', 'PUT', 'DELETE'])
def rolesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        roles = mongoDB['roles']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('roleid'):
                    filterBy['_id'] = ObjectId(request.args.get('roleid'))
                
                filterBy['company_id'] = None
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                if filterBy['company_id'] == None:
                    filterBy.pop('company_id')
                    company_list = []
                    for company in session['companies']:
                        company_list.append(ObjectId(company))
                    filterBy['company_id'] = {
                        "$in" : company_list
                    }
                returnPost = []
                companies = {}
                for role in roles.find(filterBy):
                    companyName = None
                    if role['company_id'] not in companies:
                        company_col = mongoDB['companies']
                        company = company_col.find_one({'_id':role['company_id']})
                        if company:
                                companyName = company['name']
                                companies[role['company_id']] = {"name":company['name']}
                    else:
                        companyName = companies[role['company_id']]['name']
                    roleData = convertToJSON(role)
                    roleData['company_name'] = companyName
                    returnPost.append(roleData)
                returnPost = sorted(returnPost, key = lambda i: i['company_name'])
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                postData['permissions'] = []
                role_id = simpleUpdateRow(roles, postData, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                new_lead = roles.find_one({'_id':ObjectId(role_id['id'])})
                returnPost = {
                    'message':'success',
                    'data':convertToJSON(new_lead)
                }
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            return jsonify(returnPost)
        elif request.method == 'PUT':
            try:
                updateData = request.json
                try:
                    permissions = updateData['permissions']
                    updateData.pop('permissions')
                except:
                    permissions = None
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                simpleUpdateRow(roles, updateData, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                roleID = ObjectId(updateData['id'])
                if permissions:
                    for permission in permissions:
                        search_query = {
                            "_id":roleID,
                            "permissions._id":ObjectId(permission['id'])
                        }
                        role = roles.find_one(search_query)
                        if role == None:
                            if permission['enabled'] == True:
                                permission.pop('enabled')
                                permission['_id'] = ObjectId(permission['id'])
                                permission['description'] = None
                                permission.pop('id')
                                permission.pop('role_id')
                                search_query = {
                                    "_id":roleID
                                }
                                update_query = {
                                    "$push":{
                                        "permissions":permission
                                    }
                                }
                                print(update_query)
                                roles.update_one(search_query, update_query)
                        else:
                            if permission['enabled'] == False:
                                print("Remove")

                #client.close()
                return jsonify({'Message':'Success'})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            try:
                deleteData = request.json
                role_id = simpleUpdateRow(roles, deleteData, 'DELETE', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/subscription-plans', methods=['GET', 'POST', 'PUT', 'DELETE'])
def subscriptionPlansAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        plans = mongoDB['subscription_plans']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('subid'):
                    filterBy['id'] = request.args.get('subid')
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []

                for plan in plans.find(filterBy):
                    returnPost.append(convertToJSON(plan))
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            try:
                data = request.json
                returnPost = simpleUpdateRow(plans, data, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/sales-members', methods=['GET', 'POST', 'PUT', 'DELETE'])
def salesMembersAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        salesMembers = mongoDB['sales_members']
        if request.method == 'GET':
            try:
                filterBy = {}

                if request.args.get('userid'):
                    filterBy['id'] = request.args.get('userid')

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = request.args.get('companyid')
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = session['user']['company_id']
                except:
                    pass
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []

                for user in salesMembers.find(filterBy):
                    userData = convertToJSON(user)
                    returnPost.append(userData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            try:
                data = request.json
                returnPost = simpleUpdateRow(salesMembers, data, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
    return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio', methods=['GET', 'POST', 'PUT', 'DELETE'])
def twilioAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        twilioSettings = mongoDB['twilio_numbers']
        if request.method == 'GET':
            try:
                filterBy = {}

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass

                returnPost = []
                userData = {}
                for twilio in twilioSettings.find(filterBy):
                    userData = convertToJSON(twilio)
                filterBy['_id'] = ObjectId(filterBy['company_id'])
                filterBy.pop('company_id')

                companyTwilioSettings_col = mongoDB['companies']
                companyTwilioSettings = companyTwilioSettings_col.find_one(filterBy)
                userData['twilio_enabled'] = companyTwilioSettings['twilio_enabled'],
                userData['twilio_account_sid'] = companyTwilioSettings['twilio_account_sid'],
                userData['twilio_auth_token'] = companyTwilioSettings['twilio_auth_token'],
                userData['twilio_application_sid'] = companyTwilioSettings['twilio_application_sid']
                try:
                    userData['twilio_profile_sid'] = companyTwilioSettings['twilio_profile_sid']
                except:
                    userData['twilio_profile_sid'] = None

                returnPost.append(userData)
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

        elif request.method == 'POST':
            try:
                postData = request.json
                if postData['id'] == '':
                    simpleUpdateRow(twilioSettings, postData, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                else:
                    simpleUpdateRow(twilioSettings, postData, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

        elif request.method == 'PUT':
            try:
                updateData = request.json
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                #updateRow = TwilioNumbers.query.filter_by(id=updateData['id']).update(dict(**updateData))
                #db.session.commit()
            except:
                return jsonify({'Message':'Failure'})
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/twilio/test_call', methods=['GET','POST'])
def twilioTestCallAPI():
    if validateLogin():
        if request.method == 'GET':
            try:
                twil_client = Client(str(session['call_testing']['twilio_account_sid']), str(session['call_testing']['twilio_auth_token']))
                call = twil_client.calls(str(session['call_testing']['call_id'])).fetch()
                return jsonify({'Status':str(call.status)})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']

                # GRAB COMPANY FOR TWILIO TOKENS
                companies_col = mongoDB['companies']
                filter_by = {
                    "_id":ObjectId(session['company']['id'])
                }
                company = companies_col.find_one(filter_by)

                # GRAB CAMPAIGN FOR VIRTUAL AGENT
                post_data = request.json
                campaigns_col = mongoDB['campaigns']
                filter_by = {
                    "_id":ObjectId(post_data['campaign_id'])
                }
                campaign = campaigns_col.find_one(filter_by)

                # GRAB CALLER ID
                company_caller_ids_col = mongoDB['company_caller_ids']
                filter_by = {
                    "_id":ObjectId(campaign['caller_id'])
                }
                caller_id = company_caller_ids_col.find_one(filter_by)

                # GRAB VIRTUAL AGENT FOR APP ID
                virtual_agent_col = mongoDB['virtual_agents']
                filter_by = {
                    "_id":ObjectId(campaign['virtual_agent_id'])
                }
                virtual_agent = virtual_agent_col.find_one(filter_by)

                twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])

                call = twil_client.calls.create(
                                        timeout=28,
                                        application_sid=virtual_agent['app_id'],
                                        to=post_data['reference_number'],
                                        from_=virtual_agent['phone'],
                                        caller_id=caller_id['caller_id']
                                )
                session['call_testing'] = {
                    'twilio_account_sid':company['twilio_account_sid'],
                    'twilio_auth_token':company['twilio_auth_token'],
                    'status':'calling',
                    'call_id':str(call.sid)
                }
                return jsonify({
                    'Message':'Success',
                    'data':{
                        'twilio_account_sid':company['twilio_account_sid'],
                        'twilio_auth_token':company['twilio_auth_token'],
                        'status':'calling',
                        'call_id':str(call.sid)
                    }
                })
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/available_numbers', methods=['GET', 'POST', 'PUT', 'DELETE'])
def twilioAvailableNumbersAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        companies_col = mongoDB['companies']
        filter_by = {
            "_id":ObjectId(session['company']['id'])
        }
        company = companies_col.find_one(filter_by)
        twilio_available_numbers_col = mongoDB['twilio_available_numbers']
        if request.method == 'GET':
            try:
                if request.args.get('phoneid'):
                    filter_by = {
                        "company_id":ObjectId(session['company']['id']),
                        "_id":ObjectId(request.args.get('phoneid'))
                    }
                    number = twilio_available_numbers_col.find_one(filter_by)
                    return jsonify(convertToJSON(number))
                else:
                    return_data = {
                        "purchasable_numbers":[],
                        "available_numbers":[]
                    }
                    twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                    available_numbers = None
                    if request.args.get('areacode'):
                        if str(request.args.get('areacode'))[:1] == '8':
                            available_numbers = twil_client.available_phone_numbers('US').toll_free.list(area_code=request.args.get('areacode'),limit=20)
                        else:
                            available_numbers = twil_client.available_phone_numbers('US').local.list(area_code=request.args.get('areacode'),limit=20)

                    else:
                        available_numbers = twil_client.available_phone_numbers('US').local.list(limit=20)
                    
                    for number in available_numbers:
                        return_data['purchasable_numbers'].append({
                            "phone_number":number.phone_number
                        })

                    filter_by = {
                        "company_id":ObjectId(session['company']['id'])
                    }
                    for number in twilio_available_numbers_col.find(filter_by):
                        return_data['available_numbers'].append(convertToJSON(number))

                    return jsonify(return_data)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                post_data = request.json
                twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                incoming_phone_number = twil_client.incoming_phone_numbers.create(phone_number=post_data['phone_number'])
                
                # INSERT CALLER ID DATA
                insert_data = {
                    "company_id":ObjectId(session['company']['id']),
                    "caller_id":str(post_data['phone_number'])[2:],
                    "verified":True
                }
                caller_id_col = mongoDB['company_caller_ids']
                caller_id_data = simpleUpdateRow(caller_id_col, insert_data, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))

                # INSERT TWILIO NUMBER
                insert_data = {
                    "company_id":ObjectId(session['company']['id']),
                    "phone_number":post_data['phone_number'],
                    "phone_sid":str(incoming_phone_number.sid),
                    "caller_id":ObjectId(caller_id_data['id'])
                }
                simpleUpdateRow(twilio_available_numbers_col, insert_data, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                return jsonify({"Message":"Success"})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'PUT':
            try:
                post_data = request.json
                try:
                    twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                    virtual_agent_col = mongoDB['virtual_agents']
                    virtual_agent = virtual_agent_col.find_one({"_id":ObjectId(post_data['virtual_agent_id'])})
                    incoming_phone_number = twil_client.incoming_phone_numbers(post_data['phone_sid']).update(voice_application_sid=virtual_agent['app_id'])
                except:
                    pass
                simpleUpdateRow(twilio_available_numbers_col, post_data, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                return jsonify({"Message":"Success"})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            try:
                delete_data = request.json
                try:
                    twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                    incoming_phone_number = twil_client.incoming_phone_numbers(delete_data['phone_sid']).delete()
                except:
                    return jsonify({"Message":"Failure"})
                
                twilio_available_numbers_col = mongoDB['twilio_available_numbers']
                twilio_number = twilio_available_numbers_col.find_one({"_id":ObjectId(delete_data['id'])})
                caller_id_col = mongoDB['company_caller_ids']
                caller_id_col.delete_one({"_id":twilio_number['caller_id']})
                simpleUpdateRow(twilio_available_numbers_col, delete_data, 'DELETE', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                return jsonify({"Message":"Success"})
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/usage', methods=['GET'])
def twilioUsageAPI():
    if validateLogin():
        if request.method == 'GET':
            #try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            companies_col = mongoDB['companies']
            filter_by = { 
                'twilio_account_sid' : { 
                    '$ne':None  
                } 
            }

            if request.args.get('companyid'):
                filter_by['_id'] = ObjectId(request.args.get('companyid'))

            return_post = {
                'company_summary_breakdown':{},
                'cost_breakdown':{
                    'Progammable_Voice':0,
                    'Phone_Numbers':0,
                    'Answering_Machine_Detection':0
                },
                'company_breakdown':{}
            }
            twilio_accounts = []
            
            earnings_col = mongoDB['company_wallet_earnings']
            for company in companies_col.find(filter_by):
                twilio_account_sid = company['twilio_account_sid']
                twilio_auth_token = company['twilio_auth_token']
                if twilio_account_sid not in twilio_accounts:
                    twilio_accounts.append(twilio_account_sid)
                    twil_client = Client(twilio_account_sid, twilio_auth_token)

                    company_details = {
                        "Progammable_Voice":{
                            "Speech_Recognition":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Twilio_Client_Minutes":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Recordings":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Amazon_Polly_Characters":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Conference_Minutes":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Voice_Minutes":{
                                "Inbound_Voice_Minutes":{
                                    "Inbound_Local_Calls":{
                                        "count": 0.0, 
                                        "count_unit": "", 
                                        "end_date": "", 
                                        "price": 0.0, 
                                        "price_unit": "usd", 
                                        "start_date": ""
                                    }
                                },
                                "Outbound_Voice_Minutes":{
                                    "count": 0.0, 
                                    "count_unit": "", 
                                    "end_date": "", 
                                    "price": 0.0, 
                                    "price_unit": "usd", 
                                    "start_date": ""
                                }
                            }
                        },
                        "Phone_Numbers":{
                            "Phone_Numbers":{
                                "Local_PhoneNumbers":{
                                    "count": 0.0, 
                                    "count_unit": "", 
                                    "end_date": "", 
                                    "price": 0.0, 
                                    "price_unit": "usd", 
                                    "start_date": ""
                                }
                            }
                        },
                        "Answering_Machine_Detection":{
                            "count": 0.0, 
                            "count_unit": "", 
                            "end_date": "", 
                            "price": 0.0, 
                            "price_unit": "usd", 
                            "start_date": ""
                        },
                        "Earnings":{
                            "paid_amount":0,
                            "charge_amount":0
                        }
                    }
                    # A list of record objects with the properties described above  
                    records = []

                    earning_search_query = {}
                    from_date = '2022-01-01'
                    to_date = '2022-01-31'
                    if request.args.get('type') == 'this_month':
                        records = twil_client.usage.records.this_month.list()
                        from_date = '2022-01-01'
                        to_date = '2022-01-31'
                                
                    elif request.args.get('type') == 'all_time':
                        records = twil_client.usage.records.all_time.list()
                        from_date = '2019-01-01'
                        to_date = '2122-01-31'
                                
                    elif request.args.get('type') == 'daily':
                        records = twil_client.usage.records.daily.list()
                        from_date = '2022-01-06'
                        to_date = '2022-01-06'
                                
                    elif request.args.get('type') == 'last_month':
                        records = twil_client.usage.records.last_month.list()
                        from_date = '2021-12-01'
                        to_date = '2021-12-31'
                                
                    elif request.args.get('type') == 'monthly':
                        records = twil_client.usage.records.monthly.list()
                                
                    elif request.args.get('type') == 'today':
                        records = twil_client.usage.records.today.list()
                        from_date = '2022-01-06'
                        to_date = '2022-01-06'
                                
                    elif request.args.get('type') == 'yearly':
                        records = twil_client.usage.records.yearly.list()
                                
                    elif request.args.get('type') == 'yesterday':
                        records = twil_client.usage.records.yesterday.list()

                    earning_search_query = {
                        "$and":[
                            {
                                'entry_date' : {
                                    '$gte' : from_date
                                }
                            },
                            {
                                'entry_date' : {
                                    '$lte' : to_date
                                }
                            },
                            {
                                'company_id':company['_id']
                            }
                        ]
                    }
                    print(earning_search_query)

                    earnings = earnings_col.find(earning_search_query)
                    total_paid = 0
                    total_charge = 0
                    for earning in earnings:
                        total_paid += getDecimal(earning['paid_amount'])
                        total_charge += getDecimal(earning['charge_amount'])
                    company_details['Earnings']['paid_amount'] = total_paid
                    company_details['Earnings']['charge_amount'] = total_charge

                    total = 0
                    for record in records:
                        if getDecimal(record.price) > 0 and record.category != 'totalprice':
                            if record.category == 'speech-recognition':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Speech_Recognition'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-client':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Twilio_Client_Minutes'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-recordings' or record.category == 'recordings':
                                #total += getDecimal(record.price)
                                company_details['Progammable_Voice']['Recordings'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-text-to-speech':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Amazon_Polly_Characters'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-globalconference':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Conference_Minutes'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-inbound':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Voice_Minutes']['Inbound_Voice_Minutes']['Inbound_Local_Calls'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-outbound':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Voice_Minutes']['Outbound Voice_Minutes'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'phonenumbers-local':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Phone_Numbers'] += getDecimal(record.price)
                                company_details['Phone_Numbers']['Phone_Numbers']['Local_PhoneNumbers'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'answering-machine-detection':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Answering_Machine_Detection'] += getDecimal(record.price)
                                company_details['Answering_Machine_Detection'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                    return_post['company_summary_breakdown'][str(company['_id'])] = {}
                    return_post['company_summary_breakdown'][str(company['_id'])]['billing'] = company_details
                    return_post['company_summary_breakdown'][str(company['_id'])]['details'] = {
                        'company_name':str(company['name']),
                        'company_id':str(company['_id']),
                        'total_cost':total
                    }

                    return_post['company_breakdown'][str(company['_id'])] = {
                        'company_name':str(company['name']),
                        'company_id':str(company['_id']),
                        'total_cost':total
                    }

                    #return_post['total_summary'][str(company['_id'])] = {
                    #    'company_name':str(company['name']),
                    #    'total':total
                    #}
            #return_post['company_breakdown']['summary'] = summary
            #client.close()
            return jsonify(return_post)
            #except:
            #    return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/usage/details', methods=['GET'])
def twilioUsageDetailsAPI():
    if validateLogin():
        if request.method == 'GET':
            try:
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                companies_col = mongoDB['companies']
                filter_by = {}
                if request.args.get('companyid'):
                    filter_by['_id'] = ObjectId(request.args.get('companyid'))
                else:
                    return jsonify({'Message':'Failure'})

                company = companies_col.find_one(filter_by)
                twilio_account_sid = company['twilio_account_sid']
                twilio_auth_token = company['twilio_auth_token']
                #client.close()
                twil_client = Client(twilio_account_sid, twilio_auth_token)

                return_post = []
                # A list of record objects with the properties described above
                records = []
                            
                if request.args.get('type') == 'this_month':
                    records = twil_client.usage.records.this_month.list()
                            
                elif request.args.get('type') == 'all_time':
                    records = twil_client.usage.records.all_time.list()
                            
                elif request.args.get('type') == 'daily':
                    records = twil_client.usage.records.daily.list()
                            
                elif request.args.get('type') == 'last_month':
                    records = twil_client.usage.records.last_month.list()
                            
                elif request.args.get('type') == 'monthly':
                    records = twil_client.usage.records.monthly.list()
                            
                elif request.args.get('type') == 'this_month':
                    records = twil_client.usage.records.this_month.list()
                            
                elif request.args.get('type') == 'today':
                    records = twil_client.usage.records.today.list()
                            
                elif request.args.get('type') == 'yearly':
                    records = twil_client.usage.records.yearly.list()
                            
                elif request.args.get('type') == 'yesterday':
                    records = twil_client.usage.records.yesterday.list()

                for record in records:
                    if getDecimal(record.price) > 0:
                        return_post.append({
                            'start_date':record.start_date, 
                            'end_date':record.end_date, 
                            'category':record.category, 
                            'count':getDecimal(record.count),
                            'count_unit':record.count_unit, 
                            'price':getDecimal(record.price), 
                            'price_unit':record.price_unit
                        })
                return jsonify(return_post)
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/sandbox/make_call', methods=['GET', 'POST', 'PUT'])
def twilioSandboxMakeCallAPI():
    if request.method == 'GET':
        search_query = {}
        if request.args.get('call_id'):
            search_query['call_sid'] = request.args.get('call_id')
        else:
            return jsonify({"Message":"Failure"})

        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        sandbox_conversations_col = mongoDB['sandbox_conversations']
        conversation = sandbox_conversations_col.find_one(search_query)
        return jsonify(convertToJSON(conversation))

    elif request.method == 'POST':
        post_data = request.json
        account_sid = 'ACfd0cb9bd7808a4ca590e7f163756b193'
        auth_token = '9e6c4679120eece07dde538b789a0e91'
        client = Client(account_sid, auth_token)
        application_sid = 'AP8d1aacbdf952e716245856fbff05377e'
        if post_data['campaign'] == 'obamacare':
            application_sid = 'APec30548df9926842ae9cb12ae391702b'
        elif post_data['campaign'] == 'b2b':
            application_sid = 'AP6bf4d88094593608cbce1d35b1d9dcac'
        elif post_data['campaign'] == 'auto':
            application_sid = 'AP587491edf41e0113e5c74d9d3ae8e3d7'

        call = client.calls.create(
                timeout=28,
                application_sid=application_sid,
                to=post_data['phone_number'],
                from_='+17723616669',
                caller_id='+17723616669',
                record=True,
                recording_status_callback='{}recording/callback'.format(config.webhooks),
                recording_status_callback_method='POST'
        )
        insert_data = {
            'call_sid':str(call.sid),
            'conversation':[]
        }
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        sandbox_conversations_col = mongoDB['sandbox_conversations']
        sandbox_conversations_col.insert_one(insert_data)
        #session['sandbox_call_sid'] = str(call.sid)
        print(str(call.sid))
        return jsonify({"Message":"Success", "call_sid":str(call.sid)})

    elif request.method == 'PUT':
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        sandbox_conversations_col = mongoDB['sandbox_conversations']
        post_data = request.json
        search_query = {
            'call_sid':post_data['CallSid']
        }
        update_query = {
            '$push':{
                'conversation':{
                    "owner":"client",
                    "message":post_data['user_message']
                }
            }
        }
        sandbox_conversations_col.update_one(search_query, update_query)
        for message in post_data['message']:
            update_query = {
                '$push':{
                    'conversation':{
                        "owner":"ai",
                        "message":message['text']
                    }
                }
            }
            sandbox_conversations_col.update_one(search_query, update_query)
        return jsonify({"Message":"Success"})

@apiBlueprint.route('/api/v1/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def usersAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        users = mongoDB['users']
        if request.method == 'GET':
            try:
                company_list = []
                filterBy = {}
                roleFilterBy = {}
                roleUserFilter = {}
                if request.args.get('userid'):
                    filterBy['_id'] = ObjectId(request.args.get('userid'))
                    roleUserFilter['user_id'] = ObjectId(request.args.get('userid'))

                if request.args.get('superadmin'):
                    if request.args.get('superadmin') == '1':
                        filterBy['super_admin'] = True
                    elif request.args.get('superadmin') == '0':
                        filterBy['super_admin'] = False

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        roleFilterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    else:
                        return jsonify({'Message':'Failure'})
                
                try:
                    if session['user']['company_id']:
                        roleFilterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                    
                try:
                    if session['user']['user_id'] != '613b8a785a2cd24ac1a33bc0':
                        if session['user']['company_id']:
                            roleFilterBy['company_id'] = ObjectId(session['user']['company_id'])
                        else:
                            for company in session['companies']:
                                company_list.append(ObjectId(company))
                            roleFilterBy['company_id'] = {
                                "$in" : company_list
                            }
                except:
                    pass
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass

                returnPost = {}
                returnPost['users'] = []
                roles = mongoDB['roles']
                user_ids = []
                for role in roles.find(roleFilterBy):
                    role_users = mongoDB['role_user_new']
                    roleUserFilter['role_id'] = role['_id']
                    for user in role_users.find(roleUserFilter):
                        if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
                            user_ids.append(user['user_id'])
                        else:
                            if str(user['user_id']) != '613b8a785a2cd24ac1a33bc0':
                                user_ids.append(user['user_id'])

                filterBy["_id"] = {"$in":user_ids}
                for user in users.find(filterBy):
                    roles = []
                    userData = convertToJSON(user)
                    userData['roles'] = []
                    roleUsers = mongoDB['role_user_new']
                    for roleUser in roleUsers.find({'user_id' : ObjectId(user['_id'])}):
                        filterBy = {
                            '_id':roleUser['role_id']
                        }
                        roles_col = mongoDB['roles']
                        role = roles_col.find_one(filterBy)
                        if role:
                            role_dict = convertToJSON(role)
                            role_dict.pop('permissions')
                            userData['roles'].append(role_dict)
                    returnPost['users'].append(userData)
                    
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                postData['timezone'] = 'America/New_York'
                try:
                    email = postData['email']
                    if email == None or email == '':
                        return jsonify({'Message':'Failure', 'Error':'No Email Given'})
                    user = users.find_one({'email':email})
                except:
                    return jsonify({'Message':'Failure', 'Error':'No Email Given'})
                if user:
                    return jsonify({'Message':'Failure', 'Error':'Email already registered to another user'})

                try:
                    userRoles = postData['roles']
                    postData.pop('roles')
                except:
                    userRoles = None

                try:
                    if not postData['company_id']:
                        print('Added')
                        postData['company_id'] = session['user']['company_id']
                except:
                    try:
                        postData['company_id'] = session['user']['company_id']
                    except:
                        pass
                postData['image'] = None
                postData['status'] = 'disabled'
                password = bytes(postData['password'], 'utf-8')
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password, salt)
                postData['password'] = str(hashed)[2:]
                postData['password'] = str(postData['password'])[:-1]
                newRow = simpleUpdateRow(users, postData, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                userID = newRow['id']
                if userRoles:
                    for role in userRoles:
                        role['user_id'] = userID
                        role_user_col = mongoDB['role_user_new']
                        simpleUpdateRow(role_user_col, role, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                #client.close()
                return jsonify({'Message':'Success'})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'PUT':
            try:
                updateData = request.json
                try:
                    userRoles = updateData['roles']
                    updateData.pop('roles')
                    clearRoles = updateData['clear_roles']
                    updateData.pop('clear_roles')
                except:
                    userRoles = None
                    clearRoles = False
                try:
                    password = bytes(updateData['password'], 'utf-8')
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(password, salt)
                    updateData['password'] = str(hashed)[2:]
                    updateData['password'] = str(updateData['password'])[:-1]
                except:
                    try:
                        updateData.pop('password')
                    except:
                        pass
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                simpleUpdateRow(users, updateData, 'PUT', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                userID = updateData['id']
                if userRoles:
                    role_user_col = mongoDB['role_user_new']
                    if clearRoles:
                        role_user_col.delete_many({'user_id':ObjectId(userID)})
                        for role in userRoles:
                            role['user_id'] = userID
                            filterBy = {
                                'user_id':ObjectId(role['user_id']),
                                'role_id':ObjectId(role['role_id'])
                            }
                            if not role_user_col.find_one(filterBy):
                                simpleUpdateRow(role_user_col, filterBy, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                    else:
                        for role in userRoles:
                            role['user_id'] = userID
                            filterBy = {
                                'user_id':ObjectId(role['user_id']),
                                'role_id':ObjectId(role['role_id'])
                            }
                            
                            if role_user_col.find_one(filterBy) and role['enabled'] == False:
                                simpleUpdateRow(role_user_col, filterBy, 'DELETE', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                            elif not role_user_col.find_one(filterBy) and role['enabled']:
                                simpleUpdateRow(role_user_col, filterBy, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            except:
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'DELETE':
            try:
                deleteData = request.json
                simpleUpdateRow(users, deleteData, 'DELETE', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/users/signup', methods=['POST'])
def userSignupAPI():
    if validateLogin():
        if request.method == 'POST':
            try:
                updateData = request.json
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                users_col = mongoDB['users']

                user = users_col.find_one({'_id':ObjectId(updateData['user_id'])})
                signup_tokens_col = mongoDB['signup_tokens']
                return_row = simpleUpdateRow(signup_tokens_col, updateData, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))

                
                email_settings_col = mongoDB['email_settings']
                email_filter_by = {
                    'company_id':ObjectId(updateData['company_id'])
                }
                email_setting_row = email_settings_col.find_one(email_filter_by)
                email_host = email_setting_row['mail_host'] #smtp.office365.com
                email_port = email_setting_row['mail_port'] #587
                email_username = email_setting_row['mail_username'] #info@puretalk.ai
                email_password = email_setting_row['mail_password'] #
                email_from_name = email_setting_row['mail_from_name'] #Shawn Test

                company_col = mongoDB['companies']
                company_filter_by = {
                    '_id':ObjectId(updateData['company_id'])
                }
                company_row = company_col.find_one(company_filter_by)
                company_name = company_row['name']
                company_logo = company_row['logo']

                ## EMAIL THE TOKEN #####
                s = smtplib.SMTP(host=email_host, port=email_port)
                s.starttls()
                s.login(email_username, email_password)

                msg = MIMEMultipart()
                msg['Subject'] = 'Invite Request'
                msg['From'] = email_username
                msg['To'] = user['email']
                #msg['To'] = 'shawnhasten@gmail.com'
                image_message= f"<img src='https://dashboard.puretalk.ai/static/img/brand/{company_logo}' style='width: 300px;'>"
                company_message = f"<h2><b>{company_name} has invited you to join!</b></h2>"
                anchor_message = f"<a class='btn' target='_blank' href='https://dashboard.puretalk.ai/user-sign-up?token={return_row['id']}'>Click For Access</a>"
                html_message = """
                <html>
                    <head>
                        <style>
                            body{
                                font-family: Arial, Helvetica, sans-serif;
                                background-color: #CCC;
                            }
                            .wrapper{
                                width: 600px;
                                background-color: #FFF;
                                padding: 2em;
                                text-align: center;
                            }
                            .btn{
                                text-align: center;
                                border: solid 1px #6f55ff;
                                border-radius: 3px;
                                box-sizing: border-box;
                                display: inline-block;
                                font-size: 16px;
                                font-weight: bold;
                                margin: 0;
                                border-width: 12px 25px;
                                text-decoration: none;
                                text-transform: uppercase;
                                background-color: #6f55ff;
                                color: #FFF!important;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="wrapper">
                """
                html_message += image_message
                html_message += company_message
                html_message += anchor_message
                html_message += """
                        </div>
                    </body>
                </html>
                """.format(return_row['id'])

                # Record the MIME types of both parts - text/plain and text/html.
                part2 = MIMEText(html_message, 'html')

                # Attach parts into message container.
                # According to RFC 2046, the last part of a multipart message, in this case
                # the HTML message, is best and preferred.
                msg.attach(part2)
                s.send_message(msg)
                s.quit()
                #except:
                #    pass
            except:
                return jsonify({'Message':'Failure'})
    return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/users-tour', methods=['POST'])
def usersTourAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        users = mongoDB['users']
        try:
            search_query = {
                "_id":ObjectId(session['user']['user_id'])
            }
            update_query = {
                "$set":{
                    "tour_complete":True
                }
            }
            users.update_one(search_query, update_query)
            #client.close()
            return jsonify({'Message':'Success'})
        except:
            #client.close()
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/user-img', methods=['POST'])
def userImageAPI():
    if validateLogin():
        if request.method == 'POST':
            try:
                try:
                    isthisFile=request.files.get('file')
                except:
                    return jsonify({'Message':'Failure'})
                if isthisFile:
                    newName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    fileExtention = str(isthisFile.filename).split('.')[1]
                    newFileName = newName + '.' + fileExtention

                    #client = app.mongo_client
                    mongoDB = app.mongo_client['jamesbon']
                    user_col = mongoDB['users']
                    
                    search_query = {
                        "_id":ObjectId(request.form['id'])
                    }
                    update_query = {
                        "$set": {
                            'image':newFileName
                        }
                    }
                    isthisFile.save(os.path.join(config.profile_path, newFileName))
                    user_col.update_one(search_query, update_query)
                    #client.close()
                    session['user']['image'] = newFileName
                    return jsonify({'Message':'Success'})
            except:
                return jsonify({'Message':'Failure'})
        return jsonify({'Message':'Failure'})
      
@apiBlueprint.route('/api/v1/roles-details', methods=['GET', 'POST', 'PUT', 'DELETE'])
def roleDetailsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('roleid'):
                    filterBy['_id'] = ObjectId(request.args.get('roleid'))
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                
                roles = mongoDB['roles']
                permissions = mongoDB['permissions']
                permissionList = []
                for permission in permissions.find():
                    permissionList.append({
                        'id':str(permission['_id']),
                        'name':permission['name'],
                        'display_name':permission['display_name'],
                        'allowed':False
                    })

                returnPost = []
                for role in roles.find(filterBy):
                    roleDict = convertToJSON(role)
                    allowed_permissions = roleDict['permissions']
                    roleDict['permissions'] = permissionList
                    for permission in allowed_permissions:
                        permissionDict = {
                            'id':str(permission['_id']),
                            'name':permission['name'],
                            'display_name':permission['display_name'],
                            'allowed':False
                        }
                        try:
                            indexOf = roleDict['permissions'].index(permissionDict)
                            permissionDict['allowed'] = True
                            roleDict['permissions'][indexOf] = permissionDict
                        except:
                            pass
                    returnPost.append(roleDict)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
    
@apiBlueprint.route('/api/v1/wallet/twilio', methods=['GET'])
def twilioBillingAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        companies = mongoDB['companies']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    filterBy['_id'] = ObjectId(request.args.get('companyid'))
                company = companies.find_one(filterBy)
                twilio_sub_sid = company['twilio_account_sid']
                #twilio_auth_token = company['twilio_auth_token']
                #client.close()
                #twilio_sub_sid = 'ACaec0a651b05932d0d648203e24366cfa'
                twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_SID, twilio_sub_sid)
                calls = twilio_client.calls.list(start_time_after=datetime.datetime(2021, 12, 6, 0, 0, 0), limit=4000)

                return_post = []
                for call in calls:
                    return_post.append({
                        'created_at':call.date_created,
                        'direction':call.direction,
                        'duration':call.duration,
                        'from':call.from_formatted,
                        'price':call.price,
                        'status':call.status,
                        'to_formatted':call.to_formatted,
                    })
                return jsonify(return_post)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
                    
@apiBlueprint.route('/api/v1/wallet', methods=['GET', 'POST', 'PUT'])
def walletAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        transactions = mongoDB['wallet_transactions']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('userid'):
                    filterBy['last_actioned_by'] = ObjectId(request.args.get('userid'))

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    else:
                        return jsonify({'Message':'Failure'})
                else:
                    try:
                        if session['user']['company_id']:
                            filterBy['company_id'] = ObjectId(session['user']['company_id'])
                    except:
                        return jsonify({'Message':'Failure'})
                    
                if request.args.get('from') and request.args.get('to'):
                    filterBy['updated_at'] = {
                        "$gte":request.args.get('from') + ' 00:00:00.000',
                        "$lte":request.args.get('to')+' 23:59:59.999'
                    }

                if request.args.get('type'):
                    filterBy['type'] = request.args.get('type')
                    
                limit = 1000
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []
                print(filterBy)
                for transaction in transactions.find(filterBy).sort([("created_at",pymongo.DESCENDING)]):
                    tranData = convertToJSON(transaction)
                    returnPost.append(tranData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        else:
            try:
                updateData = request.json
                #updateData['amount'] = getDecimal(updateData['amount'])
                try:
                    if session['user']['user_id']:
                        updateData['last_actioned_by'] = session['user']['user_id']
                except:
                    pass
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                returnPost = simpleUpdateRow(transactions, updateData, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/wallet/balance', methods=['GET'])
def walletBalanceAPI():
    if validateLogin():
        if request.method == 'GET':
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = request.args.get('companyid')
                    else:
                        return jsonify({'Message':'Failure'})
                else:
                    try:
                        if session['user']['company_id']:
                            filterBy['company_id'] = session['user']['company_id']
                    except:
                        pass
                
                company_wallet_balance_col = mongoDB['company_wallet_balance']
                company_wallet_balance = company_wallet_balance_col.find_one({'company_id':ObjectId(filterBy['company_id'])})
                returnBalance = {
                    "company_id":filterBy['company_id'],
                    "paid_balance":getDecimal(0),
                    "voided_balance":getDecimal(0),
                    "refunded_balance":getDecimal(0),
                    "charged_balance":getDecimal(0),
                    "balance":getDecimal(0)
                }
                if company_wallet_balance:
                    returnBalance = {
                        "company_id":str(company_wallet_balance['_id']),
                        "paid_balance":getDecimal(company_wallet_balance['paid_amount']),
                        "voided_balance":getDecimal(company_wallet_balance['voided_amount']),
                        "refunded_balance":getDecimal(company_wallet_balance['refunded_amount']),
                        "charged_balance":getDecimal(company_wallet_balance['charge_amount'])
                    }
                returnBalance['balance'] = returnBalance['paid_balance'] - returnBalance['refunded_balance'] - returnBalance['charged_balance']
                #client.close()
                return jsonify(returnBalance)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/wallet/earnings', methods=['GET'])
def walletEarningsAPI():
    if validateLogin():
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    else:
                        company_list = []
                        for company in session['companies']:
                            company_list.append(ObjectId(company))
                        filterBy['company_id'] = {
                            "$in" : company_list
                        }
                if request.args.get('from') and request.args.get('to'):
                    filterBy['entry_date'] = {
                        "$gte":request.args.get('from'),
                        "$lte":request.args.get('to')
                    }
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                company_wallet_earnings = mongoDB['company_wallet_earnings']
                returnBalance = {}
                for earning in company_wallet_earnings.find(filterBy).sort([("entry_date",pymongo.ASCENDING)]):
                    if not returnBalance.get(earning['entry_date']):
                        returnBalance[earning['entry_date']] = {
                            "company_id":str(earning['company_id']),
                            "entry_date":earning['entry_date'],
                            "paid_balance":getDecimal(earning['paid_amount']),
                            "voided_balance":getDecimal(earning['voided_amount']),
                            "refunded_balance":getDecimal(earning['refunded_amount']),
                            "charge_amount":getDecimal(earning['charge_amount'])
                        }
                    else:
                        returnBalance[earning['entry_date']]['paid_balance']+=getDecimal(earning['paid_amount'])
                        returnBalance[earning['entry_date']]['voided_balance']+=getDecimal(earning['voided_amount'])
                        returnBalance[earning['entry_date']]['refunded_balance']+=getDecimal(earning['refunded_amount'])
                        returnBalance[earning['entry_date']]['charge_amount']+=getDecimal(earning['charge_amount'])
                returnPost = []
                for key in returnBalance:
                    returnPost.append(returnBalance[key])
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/wallet/earnings_new', methods=['GET'])
def walletEarningsNewAPI():
    if validateLogin():
        if request.method == 'GET':
            #try:
            company_filter = {}
            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    company_filter['_id'] = ObjectId(request.args.get('companyid'))
                else:
                    company_list = []
                    for company in session['companies']:
                        company_list.append(ObjectId(company))
                    company_filter['_id'] = {
                        "$in" : company_list
                    }
            campaign_filter = {}
            if request.args.get('campaignid'):
                campaign_filter['campaigns._id'] = ObjectId(request.args.get('campaignid'))
            lead_filter = {}
            if request.args.get('from') and request.args.get('to'):
                lead_filter['leads.call_logs.updated_at'] = {
                    "$gte":request.args.get('from') + ' 00:00:00',
                    "$lte":request.args.get('to') + ' 23:59:59'
                }
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            companies_col = mongoDB['companies']
            pipeline = earnings_summary(company_filter=company_filter, campaign_filter=campaign_filter, lead_filter=lead_filter)
            return_post = []
            for row in companies_col.aggregate(pipeline):
                a = {}
                add_me = False
                if row['entry_date']: 
                    if request.args.get('from') and request.args.get('to'):
                        if row['entry_date'] >= request.args.get('from') and row['entry_date'] <= request.args.get('to'):
                            a = {
                                'entry_date':row['entry_date'],
                                'time_taken':row['time_taken'],
                                'charge_amount':math.ceil(row['cost'] * 100) / 100.0
                            }
                            add_me = True
                    else:
                        a = {
                            'entry_date':row['entry_date'],
                            'time_taken':row['time_taken'],
                            'charge_amount':math.ceil(row['cost'] * 100) / 100.0
                        }
                        add_me = True
                    if request.args.get('campaignid'):
                        a['campaign_id'] = request.args.get('campaignid')
                    if add_me:
                        return_post.append(a)
            #client.close()
            return jsonify(return_post)
            #except:
            #    return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/wallet/earnings/company', methods=['GET'])
def walletEarningsCompanyAPI():
    if validateLogin():
        if request.method == 'GET':
            #try:
            company_filter = {}
            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    company_filter['_id'] = ObjectId(request.args.get('companyid'))
                else:
                    company_list = []
                    for company in session['companies']:
                        company_list.append(ObjectId(company))
                    company_filter['_id'] = {
                        "$in" : company_list
                    }
            campaign_filter = {}
            if request.args.get('campaignid'):
                campaign_filter['campaigns._id'] = ObjectId(request.args.get('campaignid'))
            lead_filter = {}
            if request.args.get('from') and request.args.get('to'):
                lead_filter['leads.call_logs.updated_at'] = {
                    "$gte":request.args.get('from') + ' 00:00:00',
                    "$lte":request.args.get('to') + ' 23:59:59'
                }
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            companies_col = mongoDB['companies']
            pipeline = earnings_summary_campaign(company_filter=company_filter, campaign_filter=campaign_filter, lead_filter=lead_filter)
            return_post = []
            for row in companies_col.aggregate(pipeline):
                a = {}
                add_me = False
                if row['entry_date']: 
                    if request.args.get('from') and request.args.get('to'):
                        if row['entry_date'] >= request.args.get('from') and row['entry_date'] <= request.args.get('to'):
                            a = {
                                'entry_date':row['entry_date'],
                                'time_taken':row['time_taken'],
                                'num_calls':row['num_calls'],
                                'campaign_id':str(row['campaign_id']),
                                'charge_amount':math.ceil(row['cost'] * 100) / 100.0
                            }
                            add_me = True
                    else:
                        a = {
                            'entry_date':row['entry_date'],
                            'time_taken':row['time_taken'],
                            'num_calls':row['num_calls'],
                            'campaign_id':str(row['campaign_id']),
                            'charge_amount':math.ceil(row['cost'] * 100) / 100.0
                        }
                        add_me = True
                    if add_me:
                        return_post.append(a)
            #client.close()
            return jsonify(return_post)
            #except:
            #    return jsonify({'Message':'Failure'})
                
@apiBlueprint.route('/api/v1/payment-settings', methods=['GET', 'PUT'])
def paySettingsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        payment_gateway_settings = mongoDB['payment_gateway_settings']
        if request.method == 'GET':
            try:
                gateway = payment_gateway_settings.find_one()
                returnPost = {}

                if gateway:
                    returnPost = convertToJSON(gateway)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        elif request.method == 'PUT':
            updateData = request.json
            updateQuery = {
                "$set":{}
            }
            for key in updateData:
                updateQuery["$set"][key] = updateData[key]
            payment_gateway_settings.update_one({}, updateQuery)
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/calls/inbound', methods=['POST'])
def callInboundNewAPI():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/api/v1/calls/gathering', method='POST')
    response.append(gather)
    print(str(response))

    return Response(str(response), mimetype="text/xml")

@apiBlueprint.route('/api/v1/calls/gathering', methods=['POST'])
def callInboundGather():
    print(str(request.form))
    return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/calls/inbound/<sid>', methods=['GET', 'POST'])
def callInboundAPI(sid):
    try:
        logger.debug('Got Inbound Call: {}'.format(str(request.form)))
        print('INBOUND CALL')
        filterBy = {
            'phone':request.form['To']
        }
        logger.debug('\t Grabbing Virtual Agent Info: {}'.format(str(filterBy)))
        agent = VirtualAgents.query.filter_by(**filterBy).first()
        print(agent)
        logger.debug('\t Connecting to studio: {}'.format(agent.studio_name))
        response = VoiceResponse()
        connect = Connect(action='{}calls/events'.format(config.hostname))
        connect.virtual_agent(
            connector_name=agent.studio_name, language='en-US', status_callback='{}calls/events'.format(config.hostname)
        )
        response.append(connect)
        logger.debug('\t Studio Connected: {}'.format(agent.studio_name))
        return str(response)
    except:
        logger.debug('NO INBOUND DATA')

    return jsonify({"Message":"Failure"})

@apiBlueprint.route('/recording/callback', methods=['POST'])
def upload_recording():
    try:
        logger.debug('Got Call Back: {}'.format(str(request.form)))
        recording_url = request.form['RecordingUrl']
        logger.debug('\t Recording URL: {}'.format(str(recording_url)))

        call_id = request.form['CallSid']
        logger.debug('\t Call SID Recording: {}'.format(str(call_id)))

        recording_sid = request.form['RecordingSid']
        logger.debug('\t Recording SID: {}'.format(str(recording_sid)))

        updateData = {
            'recording_id':recording_sid,
            'recording_link':recording_url
        }
        logger.debug('\t Update Data: {}'.format(str(updateData)))
        try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads_col = mongoDB['leads']
            search_query = {
                "call_logs.call_id":call_id
            }
            update_query = {
                "$set": {
                    "call_logs.$.recording_id": recording_sid,
                    "call_logs.$.recording_link": recording_url
                }
            }
            lead = leads_col.find_one(search_query)
            leads_col.update_one(search_query, update_query)
            logger.debug('\t Committed Data')
            #client.close()
            try:
                recording_status = request.form['RecordingStatus']
                if lead['status'] == 'voicemail':
                    recording_status = 'voicemail'
                call_event = {
                    'CallStatus':recording_status,
                    'ParentCallSid':request.form['CallSid'],
                    'CallSid':request.form['CallSid'],
                    'CallDuration':request.form['RecordingDuration'],
                }
                url = '{}calls/events'.format(config.webhooks)
                requests.post(url, data=call_event)
            except:
                pass
        except:
            pass
    except:
        pass
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/calls/events', methods=['POST'])
def updateStatus():
    try:
        logger.debug('Call Events Data: {}'.format(str(request.form)))
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        campaigns_col = mongoDB['campaigns']
        company_billing_col = mongoDB['company_billing']
        wallet_transactions_col = mongoDB['wallet_transactions']
        try:

            try:
                call_status = request.form['CallStatus']
                logger.debug('\t Call Status: {}'.format(str(call_status)))
            except:
                return jsonify({"Message":"Success"}) 

            call_id_child = request.form['CallSid']
            logger.debug('\t CHILD Call SID: {}'.format(str(call_id_child)))

            try:
                call_id = request.form['ParentCallSid']
                logger.debug('\t Call SID: {}'.format(str(call_id)))
            except:
                call_id = request.form['CallSid']
                logger.debug('\t CHILD Call SID: {}'.format(str(call_id)))
            
            search_query = {
                "call_logs.call_id":call_id
            }
            logger.debug('\t Search Query: {}'.format(str(search_query)))
            update_query = {
                "$set": {
                    'call_logs.$.call_id_child':call_id_child
                }
            }
            logger.debug('\t Update Data: {}'.format(str(update_query)))
            logger.debug('\t Stage Data')
            leads_col.update_one(search_query, update_query)
            logger.debug('\t Committed Data')

            leadRow = leads_col.find_one(search_query)
            logger.debug('\t Grabbed Lead Row')

            logger.debug('\t Lead ID: {}'.format(str(leadRow['_id'])))
            update_query = {
                "$set": {}
            }
            try:
                print(call_status)
            except:
                logger.error('\t\t Failed Getting call_status')
            try:
                print(str(datetime.datetime.utcnow())[:-7])
            except:
                logger.error('\t\t Failed Getting DATETIME')
            try:
                if leadRow['call_logs'][len(leadRow['call_logs'])-1]['status'] != 'voicemail':
                    update_query = {
                        "$set": {
                            'call_logs.$.status':call_status,
                            'call_logs.$.updated_at':str(datetime.datetime.utcnow())[:-7],
                            'updated_at':str(datetime.datetime.utcnow())[:-7],
                            'status':call_status
                        }
                    }
                else:
                    update_query = {
                        "$set": {
                            'call_logs.$.updated_at':str(datetime.datetime.utcnow())[:-7],
                            'updated_at':str(datetime.datetime.utcnow())[:-7],
                            'status':call_status
                        }
                    }
            except:
                logger.error('\t\t Failed Writing update query')
            try:
                update_query["$set"]["call_logs.$.time_taken"] = getInt(request.form['CallDuration'])
                update_query["$set"]["time_taken"] = getInt(request.form['CallDuration'])
            except:
                pass
            if call_status == 'completed' or call_status == 'voicemail':
                logger.debug('\t\t Call Finished Need to charge them')
                #try:
                #    time_taken = getInt(leadRow['time_taken'])
                #except:
                #    time_taken = 0
                #update_query["$set"]["time_taken"] = getInt(time_taken)+getInt(request.form['CallDuration'])
                campaign_id = leadRow['campaign_id']
                logger.debug('\t\t Need to charge {}'.format(str(campaign_id)))
                campaignRow = campaigns_col.find_one({'_id':campaign_id})
                company_id = campaignRow['company_id']
                logger.debug('\t\t With company id {}'.format(str(company_id)))
                billing = company_billing_col.find_one({'company_id':company_id})
                if billing:
                    if call_status != 'voicemail':
                        logger.debug('\t\t Biller Found')
                        charge_amount = getDecimal(billing['charge_amount'])
                        logger.debug('\t\t Charge Amount: {}'.format(str(charge_amount)))

                        charge_type = getInt(billing['charge_type'])
                        logger.debug('\t\t Charge Type: {}'.format(str(charge_type)))
                        walletData = {}
                        call_duration = getInt(request.form['CallDuration'])
                        if charge_type == 0:
                            logger.debug('\t\t Call Duration: {}'.format(str(call_duration)))
                            if call_duration != 0:
                                minutes = getDecimal(math.ceil(call_duration/60))
                                logger.debug('\t\t Call Duration Rounded: {}'.format(str(minutes)))
                                total_charge = getDecimal(charge_amount*minutes)
                                logger.debug('\t\t Total Charge: {}'.format(str(total_charge)))
                                walletData = {
                                    'company_id':company_id,
                                    'type':'charged',
                                    'amount':getDecimal(total_charge)
                                }
                        else:
                            if call_duration > 3:
                                total_charge = getDecimal(charge_amount)
                                logger.debug('\t\t Total Charge: {}'.format(str(total_charge)))
                                walletData = {
                                    'company_id':company_id,
                                    'type':'charged',
                                    'amount':getDecimal(total_charge)
                                }

                        try:
                            walletData['memo'] = 'Campaign ID: {} calling: {}'.format(str(campaign_id), str(leadRow['reference_number']))
                        except:
                            pass
                        logger.debug('\t\t Wallet Data: {}'.format(str(walletData)))
                        simpleUpdateRow(wallet_transactions_col, walletData, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                        logger.debug('\t\t Stage Data')
                        logger.debug('\t\t Committed Data')
                else:
                    logger.error('\t\t Cannot Find Billing')
            #elif call_status == 'answered':
            #    logger.debug('\t Set the call to answered: {}'.format(str(update_query)))
            #    search_query = {
            #        "call_logs.call_id":call_id
            #    }
            #    logger.debug('\t Search Query: {}'.format(str(search_query)))
            #    update_query = {
            #        "$set": {
            #            'call_logs.$.answered':True
            #        }
            #    }
            #    logger.debug('\t Update Data: {}'.format(str(update_query)))
            #    logger.debug('\t Stage Data')
            #    leads_col.update_one(search_query, update_query)

            logger.debug('\t Search Query: {}'.format(str(search_query)))
            logger.debug('\t Lead Update Data: {}'.format(str(update_query)))
            leads_col.update_one(search_query, update_query)
        except:
            pass
        #client.close()
    except:
        pass
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/calls/amd', methods=['POST'])
def updateAMD():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        logger.debug('AMD Data: {}'.format(str(request.form)))
        if request.form['AnsweredBy'] != 'human':
            call_id = request.form['CallSid']
            search_query = {
                "call_logs.call_id":call_id
            }
            lead_row = leads_col.find_one(search_query)
            campaigns_col = mongoDB['campaigns']
            campaign = campaigns_col.find_one({'_id':lead_row['campaign_id']})
            companies_col = mongoDB['companies']
            company = companies_col.find_one({'_id':campaign['company_id']})
            account_sid = company['twilio_account_sid']
            auth_token = company['twilio_auth_token']
            try:
                twilClient = Client(account_sid, auth_token)
                logger.debug('\t Call To Hang Up: {}'.format(str(call_id)))

                logger.debug('\t Attempting To Hang Up Call')
                thisCall = twilClient.calls(call_id).update(twiml='<Response><Hangup/></Response>')
                logger.debug('\t Call Hung Up')
            except:
                pass

            logger.debug('\t Grabbing Lead Info')
            search_query = {
                "call_logs.call_id":str(call_id)
            }
            update_query = {
                "$set": {
                    'call_logs.$.status':'voicemail',
                    'status':'voicemail'
                }
            }
            logger.debug('\t Search Query: {}'.format(str(search_query)))
            logger.debug('\t Lead Update Data: {}'.format(str(update_query)))
            leads_col.update_one(search_query, update_query)
            #leadCall = LeadCalls.query.filter(or_(LeadCalls.call_id == call_id, LeadCalls.call_id_child == call_id)).first()
            #leadID = leadCall.lead_id
            #logger.debug('\t Lead ID: {}'.format(leadID))
            #
            #updateData = {
            #    'status':'voicemail'
            #}
            #updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
            #logger.debug('\t Lead Update Data: {}'.format(str(updateData)))
            #updateRow = Leads.query.filter_by(id=leadID).update(dict(**updateData))
            #logger.debug('\t Stage Data')
            #db.session.commit()
            logger.debug('\t Committed Data')
        #client.close()
    except:
        pass
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/calls/interested', methods=['POST'])
def updateInterest():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        post_data = request.json
        logger.debug('Interest Data: {}'.format(str(request.json)))
        leads_col = mongoDB['leads']

        # Update Lead as interested
        search_query = {
            "call_logs.call_id":post_data['CallSid']
        }
        update_query = {
            '$set':{
                'interested':'interested'
            }
        }
        leads_col.update_one(search_query,update_query)
        
        # Check for webhook to transfer lead data
        lead = leads_col.find_one(search_query)
        campaigns_col = mongoDB['campaigns']
        campaign = campaigns_col.find_one({'_id':lead['campaign_id']})

        logger.debug('\t Stop recording')
        companies_col = mongoDB['companies']
        company = companies_col.find_one({'_id':campaign['company_id']})
        try:
            try:
                twilio_account_sid = company['twilio_account_sid']
                logger.debug('\t\t Account SID: {}'.format(twilio_account_sid))
            except:
                logger.error('\t\t Failed Grabbing Account SID')
            try:
                twilio_auth_token = company['twilio_auth_token']
                logger.debug('\t\t Auth Token: {}'.format(twilio_auth_token))
            except:
                logger.error('\t\t Failed Grabbing Auth Token')
            try:
                twil_client = Client(twilio_account_sid, twilio_auth_token)
                logger.debug('\t\t Created Twil Client')
            except:
                logger.error('\t\t Failed Creating Twil Client')
            try:
                logger.debug('\t\t Find Recording Using: {}'.format(str(post_data['CallSid'])))
                recording = twil_client.calls(str(post_data['CallSid'])).recordings.list(limit=1)
                try:
                    logger.debug('\t\t Find Total Of {} Recordings'.format(str(len(recording))))
                except:
                    pass
                recording_id = str(recording[0].sid)
                logger.debug('\t\t Recording ID: {}'.format(recording_id))
            except:
                logger.error('\t\t Failed Grabbing Recording ID')
            try:
                twil_client.calls(str(post_data['CallSid'])).recordings(recording_id).update(status='stopped')
                logger.debug('\t Stop Record Successful')
            except:
                logger.error('\t\t Failed Sending Stop Request')
        except:
            logger.error('\t Failed to stop recording')
        try:
            ## DO TRANSFER WEBHOOK STUFF #########
            webhook_url = campaign['xfer_url']
            webhook_data = {}
            for data in lead['lead_data']:
                try:
                    webhook_data[data['field_name']] = data['field_value']
                except:
                    pass
            requests.post(webhook_url, json=webhook_data)
        except:
            pass
        #client.close()
        return jsonify({"Message":"Success"})
    except:
        return jsonify({"Message":"Failure"})

@apiBlueprint.route('/calls/dnc', methods=['POST'])
def updateLeadDNC():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        post_data = request.json
        logger.debug('DNC Data: {}'.format(str(request.json)))
        leads_col = mongoDB['leads']

        # Update Lead as Do Not Call
        search_query = {
            "call_logs.call_id":post_data['CallSid']
        }
        update_query = {
            '$set':{
                'dnc':True
            }
        }
        leads_col.update_one(search_query,update_query)
        return jsonify({"Message":"Success"})
    except:
        return jsonify({"Message":"Failure"})

@apiBlueprint.route('/calls/voicemail', methods=['POST'])
def updateLeadVoicemail():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        post_data = request.json
        logger.debug('Voicemail Data: {}'.format(str(request.json)))
        leads_col = mongoDB['leads']

        # Update Lead as Do Not Call
        search_query = {
            "call_logs.call_id":post_data['CallSid']
        }
        update_query = {
            "$set": {
                'status':'voicemail',
                'call_logs.$.status':'voicemail'
            }
        }
        leads_col.update_one(search_query,update_query)
        return jsonify({"Message":"Success"})
    except:
        return jsonify({"Message":"Failure"})

@apiBlueprint.route('/agent/hooks', methods=['GET'])
def localAgentHookGet():
    if request.method == 'GET':
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        lead_hooks_col = mongoDB['lead_hooks']
        search_query = {
            "campaign_id":session['agent-campaign'],
            "checked":False
        }
        lead_hook = lead_hooks_col.find_one(search_query)
        if lead_hook:
            search_query = {
                "_id":ObjectId(lead_hook['_id'])
            }
            update_query = {
                "$set":{
                    "checked":True
                }
            }
            lead_hooks_col.update_one(search_query, update_query)
            return jsonify({"Message":"Success", "details":convertToJSON(lead_hook)})
    return jsonify({"Message":"Failure"})

@apiBlueprint.route('/agent/hooks/<token>', methods=['POST'])
def localAgentHookPost(token):
    if request.method == 'POST':
        try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads_col = mongoDB['leads']
            search_query = {
                "call_logs.call_id":request.form.get('CallSid')
            }
            lead = leads_col.find_one(search_query)
            if lead:
                logger.debug('Local Agent Hook Data: {}'.format(str(request.json)))

                try:
                    ## DO TRANSFER WEBHOOK STUFF #########
                    lead_hooks_col = mongoDB['lead_hooks']
                    insert_query = {
                        "checked":False,
                        "details":lead['lead_data'],
                        "campaign_id":str(lead['campaign_id']),
                        "created_at":str(datetime.datetime.utcnow())[:-3],
                        "updated_at":str(datetime.datetime.utcnow())[:-3]
                    }
                    lead_hooks_col.insert_one(insert_query)
                except:
                    pass
                #client.close()
            return jsonify({"Message":"Success"})
        except:
            return jsonify({"Message":"Failure"})

@apiBlueprint.route('/api/v1/stripe/charge', methods=['POST'])
def make_stripe_charge():
    if request.method == 'POST':
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        transactions = mongoDB['wallet_transactions']

        post_data = request.json
        try:
            company_id = post_data['company_id']
        except:
            try:
                company_id = session['company']['id']
            except:
                return jsonify({'Message':'Failure'})
        type = post_data['type']
        customer_name = post_data['customer_name']
        customer_email = post_data['customer_email']
        #customer_address = post_data['customer_address']
        #customer_city = post_data['customer_city']
        #customer_state = post_data['customer_state']
        #customer_zip = post_data['customer_zip']
        #customer_country = post_data['customer_country']

        card_number = post_data['card_number']
        card_exp_month = post_data['card_exp_month']
        card_exp_year = post_data['card_exp_year']
        card_cvc = post_data['card_cvc']

        amount = post_data['amount']
        customer_memo = post_data['memo']

        stripe.api_key = "sk_test_51JegctKAR6Ijtm4HWZnH2WM2eHgbTroDNlU0fn1apFsStYw2e0HeHYWXqRQMvpwLIMnnTKjwl57DbwlP6JOc4BFX00ZftJ7zJN"
        try:
            card_token = stripe.Token.create(
                card={
                    "number": card_number,
                    "exp_month": getInt(card_exp_month),
                    "exp_year": getInt(card_exp_year),
                    "cvc": card_cvc,
                }
            )
        except:
            return jsonify({'Message':'Card number was not valid!'})

        print("Attempting charge...")

        try:
            resp = stripe.Charge.create(
                amount=getInt(amount)*100,
                currency="usd",
                card=card_token,
                description=customer_email,
            )
        except:
            return jsonify({'Message':'Charge failed!'})

        if resp['status'] == 'succeeded':
            updateData = {
                'company_id':company_id,
                'type':'paid',
                'amount':getDecimal(post_data['amount']),
                'created_at':str(datetime.datetime.utcnow())[:-3],
                'updated_at':str(datetime.datetime.utcnow())[:-3],
                'memo':customer_memo
            }
            try:
                updateData['payment_method_details'] = resp['payment_method_details']
            except:
                pass
            try:
                if session['user']['user_id']:
                    updateData['last_actioned_by'] = session['user']['user_id']
            except:
                pass
            returnPost = simpleUpdateRow(transactions, updateData, 'POST', str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            #client.close()
            return jsonify(returnPost)

        #client.close()
        return jsonify({'Message':'Charge failed!'})