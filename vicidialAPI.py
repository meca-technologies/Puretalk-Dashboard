from flask import Flask, json, jsonify, request, Blueprint, send_file
from flask_httpauth import HTTPBasicAuth as Flask_HTTPBasicAuth
from app import session
import datetime
import pytz
from dateutil.relativedelta import relativedelta
import pymongo

from werkzeug.utils import redirect

import bcrypt

viciApiBlueprint = Blueprint('viciAPI', __name__)

import requests
from requests.auth import HTTPBasicAuth

import config
from pyAreadCodes import areaCodeTZ
from pyStateLaws import stateLaws

import string
import random
import os
import math
from bson.objectid import ObjectId

import stripe


from app import logger

import numpy as np
import pandas as pd

import pyAreadCodes
import pyPostalCodes

from sqlescapy import sqlescape
import math
from decimal import *

import pymysql.cursors

auth = Flask_HTTPBasicAuth()

server = 'http://www.vicidial.org/vicidial_demo'

def getConnection(host, user, passwd, db='asterisk'):
    return pymysql.connect(host=host,
                             port=3306,
                             user=user,
                             password=passwd,
                             database=db,
                             cursorclass=pymysql.cursors.DictCursor)

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
            return True
            return False
    except:
        return True
        return False

def validateCompany(companyID):
    try:
        if str(companyID) in session['companies']:
            return True
    except:
        pass
    return False

def url_builder(server, function, params):
    url = '{}/non_agent_api.php?function={}'.format(server, function)
    for param in params:
        url += '&{}={}'.format(param, params[param])
    return url

def url_builder_new(server, function, params):
    url = '{}/puretalk_api.php?function={}'.format(server, function)
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

def csv_writer_multi(data, delimiter='|'):
    return_data_full = []
    try:
        split_data_full = data.split('--BREAK--')
        for split_data in split_data_full:
            return_data = []
            rows = split_data.split('\n')
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
            return_data_full.append(return_data)
    except:
        return_data = {'Message':'Couldn\'t Parse Data'}
    return return_data_full

def sql_writer(queries, server, user, password):
    for query in queries:    
        url = url_builder(server, 'general_purpose', [])
        url += '&user='+user
        url += '&pass='+password
        url += '&sql_query='+query

        response = requests.get(url)
        req_data = response.text
        print(req_data)
    return 'Success'

def insert_writer(value, obj):
    try:
        if value == 'phone_number':
            try:
                return obj[value]
            except:
                return obj['PHONE NUMBER']
        elif value == 'first_name':
            try:
                return obj[value]
            except:
                return obj['FIRST NAME']
        elif value == 'last_name':
            try:
                return obj[value]
            except:
                return obj['LAST NAME']
        elif value == 'email':
            try:
                return obj[value]
            except:
                return obj['EMAIL']
        elif value == 'phone_code':
            return 1
        else:
            return obj[value]
    except:
        return ''

@viciApiBlueprint.route('/api/vici/campaigns-old', methods=['GET', 'POST', 'PUT'])
def viciGetCampaigns():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            
            url = url_builder(server, 'campaigns_list', request.args)
            url += '&user='+user
            url += '&pass='+password
            client.close()

            response = requests.get(url)
            req_data = 'campaign_id,campaign_name,active,user_group,dial_method,dial_level,lead_order,dial_statuses\n'
            req_data += response.text

            data = csv_writer(req_data, ',')

            return jsonify({
                'data':data,
                'url':url
            })
        elif request.method == 'POST':
            #client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            #mongoDB = client['jamesbon']
            #companies_col = mongoDB['companies']
            #company = companies_col.find_one({'_id':session['company']['id']})
            #server = company['vici_server']
            #user = company['vici_user']
            #password = company['vici_password']
            #client.close()

            server = 'http://216.244.65.82/vicidial'
            user = '6666'
            password = 'admin1234'

            req_form = request.form
            url = '{}/admin.php'.format(server)

            headers = {
                'Content-Disposition': 'form-data',
                'Content-Type': 'text/xml'
            }
            req = requests.post(url, auth=HTTPBasicAuth(user, password), headers=headers, data=req_form)
            print(req.text)
            if req.text == 'Login incorrect, please try again: |user|pass|BAD|\n':
                return jsonify({
                    'Message':'Failure',
                    'url':url
                })
            else:
                return jsonify({
                    'Message':'Success',
                    'url':url
                })
        elif request.method == 'PUT':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            company = companies_col.find_one({'_id':session['company']['id']})
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            update_json = request.json
            url = '{}/non_agent_api.php?function={}&campaign_id={}'.format(server, 'update_campaign', update_json['campaign_id'])
            update_json.pop('campaign_id')
            update_json['user'] = user
            update_json['pass'] = password
            for x in update_json:
                url+='&{}={}'.format(x, update_json[x])
            
            response = requests.get(url)
            
            return jsonify({
                'data':response.text,
                'url':url
            })
    return jsonify({'Message':"Failure"})

@viciApiBlueprint.route('/api/vici/lists', methods=['GET', 'POST', 'PUT', 'DELETE'])
def viciGetLists():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            list_list = getAllLists(session['company']['id'], 'str')

            client.close()
            
            url = url_builder_new(server, 'lists_get', [])
            url += '&list_list='+list_list
            url += '&user='+user
            url += '&pass='+password

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')

            return jsonify({
                'data':data,
                'url':url
            })

        elif request.method == 'POST':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            url = url_builder_new(server, 'lists_post', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&list_id='+post_data['list_id']
            url += '&list_name='+post_data['list_name']
            url += '&campaign_id='+post_data['campaign_id']
            url += '&active='+post_data['active']
            url += '&list_description='+post_data['list_description']

            response = requests.get(url)
            req_data = response.text

            insert_query = {
                "company_id":session['company']['id'],
                "list_id":post_data['list_id']
            }
            list_members_col = mongoDB['list_members']
            list_members_col.insert_one(insert_query)
            client.close()
            
            return  jsonify({'Message':req_data})
            
        elif request.method == 'PUT':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            

            url = url_builder_new(server, 'lists_put', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&active='+post_data['active']
            url += '&campaign_name='+post_data['campaign_name']
            url += '&dial_timeout='+post_data['dial_timeout']
            url += '&campaign_cid='+post_data['campaign_cid']

            response = requests.get(url)
            req_data = response.text

            insert_query = {
                "company_id":session['company']['id'],
                "list_id":str(post_data['list_id'])
            }
            list_members_col = mongoDB['list_members']
            if not list_members_col.find_one(insert_query):
                list_members_col.insert_one(insert_query)

            client.close()
            
            return  jsonify({'Message':req_data})
            
        elif request.method == 'DELETE':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            

            url = url_builder_new(server, 'lists_delete', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&list_id='+post_data['list_id']

            response = requests.get(url)
            req_data = response.text

            return  jsonify({'Message':req_data})

    return jsonify({'Message':"Failure"})

@viciApiBlueprint.route('/api/vici/campaign_lists', methods=['GET'])
def viciGetCampaignLists():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            
            url = url_builder(server, 'vicidial_campaigns_list', request.args)
            url += '&user='+user
            url += '&pass='+password
            client.close()

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')

            return jsonify({
                'data':data,
                'url':url
            })
    return jsonify({'Message':"Failure"})

@viciApiBlueprint.route('/api/vici/campaigns', methods=['GET', 'POST', 'PUT', 'DELETE'])
def viciGetCampaignsV2():
    if validateLogin():
        if request.method == 'GET':
            try:   
                client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                mongoDB = client['jamesbon']
                companies_col = mongoDB['companies']
                search_query = {
                    '_id':ObjectId(session['company']['id'])
                }
                company = companies_col.find_one(search_query)
                server = company['vici_server']
                user = company['vici_user']
                password = company['vici_password']

                campaign_list = getAllCampaigns(session['company']['id'], 'str')

                client.close()
                
                url = url_builder_new(server, 'campaigns_get', [])
                url += '&campaign_list='+campaign_list
                url += '&user='+user
                url += '&pass='+password

                response = requests.get(url)
                req_data = response.text

                data = csv_writer_multi(req_data, ',')

                return_data = {}
                for x in data[0]:
                    if not return_data.get(x['campaign_id']):
                        status = 'STOPPED'
                        if x['status'] == 'ACTIVE':
                            status = 'RUNNING'
                        return_data[x['campaign_id']] = {
                            "call_count":0,
                            "lead_count":0,
                            "remaining_leads":0,
                            "number_of_lines":x['number_of_lines'],
                            "status":status
                        }
                        return_data[x['campaign_id']]['lists'] = []
                    list_obj = x
                    list_obj['call_count'] = float(x['call_count'])
                    return_data[x['campaign_id']]['lists'].append(x)
                    return_data[x['campaign_id']]['call_count'] += float(x['call_count'])
                    return_data[x['campaign_id']]['lead_count'] += float(x['tally'])
                    return_data[x['campaign_id']]['remaining_leads'] = float(return_data[x['campaign_id']]['lead_count'] - return_data[x['campaign_id']]['call_count'])

                return_data_full = []
                for row in data[1]:
                    dict_obj = {}
                    for col in row:
                        dict_obj[col] = row[col]
                    return_data_full.append(dict_obj)

                for x in range(0, len(return_data_full)):
                    try:
                        return_data_full[x]['extra_detail'] = return_data[return_data_full[x]['campaign_id']]
                        return_data_full[x]['number_of_lines'] = return_data[return_data_full[x]['campaign_id']]['number_of_lines']
                    except:
                        return_data_full[x]['extra_detail'] = {}

                return jsonify({
                    'data':return_data_full,
                    'url':url
                })
            except:
                return jsonify({'Message': 'Failure'})
        elif request.method == 'POST':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            
            vicidial_server_trim = server.replace('http://', '')
            vicidial_server_trim = vicidial_server_trim.replace('https://', '')
            vicidial_server_trim = vicidial_server_trim.replace('/vicidial', '')

            url = url_builder_new(server, 'campaigns_post', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&campaign_id='+post_data['campaign_id']
            url += '&campaign_name='+post_data['campaign_name']
            url += '&campaign_description='+post_data['campaign_description']
            url += '&active='+post_data['active']
            url += '&park_ext='+post_data['park_ext']
            url += '&park_file_name='+post_data['park_file_name']
            url += '&allow_closers='+post_data['allow_closers']
            url += '&hopper_level='+post_data['hopper_level']
            url += '&auto_dial_level='+post_data['auto_dial_level']
            url += '&next_agent_call='+post_data['next_agent_call']
            url += '&local_call_time='+post_data['local_call_time']
            url += '&voicemail_ext='+post_data['voicemail_ext']
            url += '&script_id='+post_data['script_id']
            url += '&get_call_launch='+post_data['get_call_launch']
            url += '&user_group='+post_data['user_group']
            url += '&campaign_script_two='+post_data['campaign_script_two']
            url += '&vicidial_server_trim='+vicidial_server_trim

            response = requests.get(url)
            req_data = response.text

            insert_query = {
                "company_id":session['company']['id'],
                "campaign_id":post_data['campaign_id']
            }
            campaign_members_new_col = mongoDB['campaign_members_new']
            campaign_members_new_col.insert_one(insert_query)
            client.close()

            return  jsonify({'Message':req_data})
        elif request.method == 'PUT':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            

            url = url_builder_new(server, 'campaigns_put', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&campaign_id='+post_data['campaign_id']
            url += '&campaign_name='+post_data['campaign_name']
            url += '&dial_timeout='+post_data['dial_timeout']
            url += '&campaign_cid='+post_data['campaign_cid']
            url += '&hopper_level='+post_data['hopper_level']
            url += '&campaign_cid='+post_data['campaign_cid']
            url += '&cid_group_id='+post_data['cid_group_id']
            url += '&xferconf_a_dtmf='+post_data['xferconf_a_dtmf']
            url += '&active='+post_data['active']

            response = requests.get(url)
            req_data = response.text

            insert_query = {
                "company_id":session['company']['id'],
                "campaign_id":post_data['campaign_id']
            }
            campaign_members_new_col = mongoDB['campaign_members_new']
            if not campaign_members_new_col.find_one(insert_query):
                campaign_members_new_col.insert_one(insert_query)

            return  jsonify({'Message':req_data})
        elif request.method == 'DELETE':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            

            url = url_builder_new(server, 'campaigns_delete', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&campaign_id='+post_data['campaign_id']

            response = requests.get(url)
            req_data = response.text
            print(req_data)

            return  jsonify({'Message':req_data})
            #return  jsonify({'Message':'Success'})

    return jsonify({'Message':"Failure"})

@viciApiBlueprint.route('/api/vici/call_by_date', methods=['GET', 'POST', 'PUT', 'DELETE'])
def viciGetCallsByDate():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()
            
            list_list = getAllLists(session['company']['id'], 'str')
            url = url_builder_new(server, 'calls_by_date', [])
            url += '&list_list='+list_list
            url += '&user='+user
            url += '&pass='+password
            if request.args.get('from') and request.args.get('to'):
                url += '&from='+request.args.get('from')
                url += '&to='+request.args.get('to')

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')

            return_data = []
            for x in data:
                return_data.append({
                    "count":x['lead_count'],
                    "full_date":str(x['call_date_full'])
                })
            return jsonify(return_data)

@viciApiBlueprint.route('/api/vici/call_summary_two', methods=['GET'])
def viciGetCallSummaryTwo():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()
        
            list_list = getAllLists(session['company']['id'], 'str')
            query = '''
            SELECT status
                ,COUNT(status) as count_status
                ,SUM(length_in_sec) as call_time
            FROM vicidial_log vl
            WHERE 
            '''.format(list_list)
            if request.args.get('from') and request.args.get('to'):
                query += "call_date BETWEEN '{}' and '{}' AND ".format(sqlescape(request.args.get('from')),sqlescape(request.args.get('to')))
            query += '''
            list_id in ({})
            GROUP BY status
            '''.format(list_list)

            return_data = {
                'statuses':[],
                'interest_breakdown':[],
                'billing':{
                    "campaign_minute_breakdown": [],
                    "charge_amount": 0
                }
            }
            total_call_time = 0
            total_calls = 0
            total_calls_xfer = 0
            connection = getConnection('216.244.65.82', 'cron', 'fds56FDSsdf576FSD', 'asterisk')
            with connection:
                with connection.cursor() as cursor:
                    ## GETTING LISTS #############################################################################################################################
                    cursor.execute(query)
                    for x in cursor:
                        total_call_time += getInt(x['call_time'])
                        total_calls += getInt(x['count_status'])
                        if x['status'] == 'XFER':
                            total_calls_xfer = getInt(x['count_status'])
                        return_data['statuses'].append({
                            "count":x['count_status'],
                            "status":x['status']
                        })
                    return_data['total_call_time'] = total_call_time
                    return_data['total_calls'] = total_calls
                    return_data['total_calls_made'] = total_calls_xfer
                    return_data['total_calls_xfer'] = total_calls_xfer

                    ## INTEREST BREAKDOWN #################################################################
                    query = '''
                    SELECT SUM(status_count) as total
                        ,MAX(interest) as interested
                        ,campaign_id
                        FROM (
                            SELECT status_count
                                ,CASE 
                                    WHEN status = 'XFER' THEN status_count
                                END as interest
                                ,campaign_id
                            FROM (
                                SELECT status as status
                                    ,COUNT(vc.status) as status_count
                                    ,vl.campaign_id as campaign_id 
                                FROM vicidial_log vc
                                LEFT JOIN vicidial_lists vl
                                ON vc.list_id = vl.list_id 
                                WHERE
                    '''.format(list_list)
                    if request.args.get('from') and request.args.get('to'):
                        query += "call_date BETWEEN '{}' and '{}' AND ".format(sqlescape(request.args.get('from')),sqlescape(request.args.get('to')))
                    query += '''
                            vl.list_id in ({})
                            GROUP BY vl.campaign_id, vc.status
                        ) as a
                    ) as b
                    '''.format(list_list)
                    cursor.execute(query)
                    for x in cursor:
                        return_data['interest_breakdown'].append({
                            'campaign_id': x['campaign_id'], 
                            'interested': getInt(x['interested']), 
                            'total': getInt(x['total'])
                        })

                    ## BILLING BREAKDOWN #################################################################
                    query = '''
                    SELECT SUM(CEILING(CAST((length_in_sec) AS INT) / 60)) as minutes
                        ,SUM(length_in_sec) as total_seconds
	                    ,vl.campaign_id 
                    FROM vicidial_log vc
                    LEFT JOIN vicidial_lists vl
                    ON vc.list_id = vl.list_id 
                    WHERE length_in_sec > 2
                    '''.format(list_list)
                    if request.args.get('from') and request.args.get('to'):
                        query += " AND call_date BETWEEN '{}' AND '{}' AND ".format(sqlescape(request.args.get('from')),sqlescape(request.args.get('to')))
                    query += '''
                    vl.list_id in ({})
                    GROUP BY vl.campaign_id
                    '''.format(list_list)
                    cursor.execute(query)
                    total_charge = 0
                    for x in cursor:
                        total_charge -= getInt(x['minutes'])*.25
                        return_data['billing']['campaign_minute_breakdown'].append({
                            'campaign_id': x['campaign_id'], 
                            'rounded_minutes': getInt(x['minutes']), 
                            'total_charge': getInt(x['minutes'])*.25
                        })
                    return_data['billing']['charge_amount'] = total_charge
            
            return jsonify({'data':return_data})

@viciApiBlueprint.route('/api/vici/call_summary', methods=['GET'])
def viciGetCallSummary():
    if validateLogin():
        if request.method == 'GET':   
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            list_list = getAllLists(session['company']['id'], 'str')

            client.close()
            
            url = url_builder_new(server, 'call_summary', [])
            url += '&list_list='+list_list
            url += '&user='+user
            url += '&pass='+password
            if request.args.get('from') and request.args.get('to'):
                url += '&from='+request.args.get('from')
                url += '&to='+request.args.get('to')

            response = requests.get(url)
            req_data = response.text

            data = csv_writer_multi(req_data, ',')

            return_data = {
                'statuses':[],
                'interest_breakdown':[],
                'billing':{
                    "campaign_minute_breakdown": [],
                    "charge_amount": 0
                }
            }
            total_call_time = 0
            total_calls = 0
            total_calls_xfer = 0

            for x in data[0]:
                total_call_time += getInt(x['call_time'])
                total_calls += getInt(x['count_status'])
                if x['status'] == 'XFER':
                    total_calls_xfer = getInt(x['count_status'])
                return_data['statuses'].append({
                    "count":x['count_status'],
                    "status":x['status']
                })
            return_data['total_call_time'] = total_call_time
            return_data['total_calls'] = total_calls
            return_data['total_calls_made'] = total_calls_xfer
            return_data['total_calls_xfer'] = total_calls_xfer
            
            for x in data[1]:
                return_data['interest_breakdown'].append({
                    'campaign_id': x['campaign_id'], 
                    'interested': getInt(x['interested']), 
                    'total': getInt(x['total'])
                })

            total_charge = 0
            for x in data[2]:
                total_charge -= getInt(x['minutes'])*.25
                return_data['billing']['campaign_minute_breakdown'].append({
                    'campaign_id': x['campaign_id'], 
                    'rounded_minutes': getInt(x['minutes']), 
                    'total_charge': getInt(x['minutes'])*.25
                })
            return_data['billing']['charge_amount'] = total_charge
            
            return jsonify({'data':return_data})

@viciApiBlueprint.route('/api/vici/campaigns_control', methods=['POST'])
def viciGetCampaignsControl():
    if validateLogin():
        if request.method == 'POST':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()

            url = url_builder_new(server, 'campaigns_control', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&status='+post_data['status']
            url += '&campaign_id='+post_data['campaign_id']

            response = requests.get(url)
            req_data = response.text
            
            return  jsonify({'Message':req_data})
    return jsonify({'Message':"Failure"})

@viciApiBlueprint.route('/api/vici/caller_id_groups', methods=['GET', 'POST', 'PUT', 'DELETE'])
def viciGetCallerIDGroups():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()
            
            url = url_builder_new(server, 'caller_id_groups_get', [])
            url += '&user='+user
            url += '&pass='+password

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')

            return jsonify({
                'data':data,
                'url':url
            })
        elif request.method == 'POST':
            post_data = request.json

            return  jsonify({'Message':'Success'})

    return jsonify({'Message':"Failure"})
    
@viciApiBlueprint.route('/api/vici/caller_ids', methods=['GET', 'POST', 'PUT', 'DELETE'])
def viciGetCallerIDs():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()
            
            url = url_builder_new(server, 'caller_ids_get', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&group_id='+request.args.get('group_id')

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')

            return jsonify({
                'data':data,
                'url':url
            })
        elif request.method == 'POST':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()

            url = url_builder_new(server, 'caller_ids_post', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&group_id='+post_data['group_id']
            url += '&areacode='+post_data['areacode']
            url += '&outbound_cid='+post_data['outbound_cid']
            url += '&cid_description='+post_data['cid_description']

            response = requests.get(url)
            req_data = response.text

            return  jsonify({'Message':req_data})
        elif request.method == 'PUT':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()

            url = url_builder_new(server, 'caller_ids_put', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&active='+post_data['active']
            url += '&group_id='+post_data['group_id']
            url += '&outbound_cid='+post_data['outbound_cid']

            response = requests.get(url)
            req_data = response.text

            return  jsonify({'Message':req_data})
        elif request.method == 'DELETE':
            post_data = request.json
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()

            url = url_builder_new(server, 'caller_ids_delete', [])
            url += '&user='+user
            url += '&pass='+password
            url += '&group_id='+post_data['group_id']
            url += '&outbound_cid='+post_data['outbound_cid']

            response = requests.get(url)
            req_data = response.text

            return  jsonify({'Message':req_data})

    return jsonify({'Message':"Failure"})

@viciApiBlueprint.route('/api/vici/leads', methods=['GET', 'POST'])
def viciGetLeadData():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            client.close()
            
            url = url_builder_new(server, 'leads_get', [])
            url += '&list_id='+request.args.get('list_id')
            url += '&user='+user
            url += '&pass='+password

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')

            return jsonify({
                'data':data,
                'url':url
            })
        elif request.method == 'POST':
            orig_data = request.json
            max_length = len(orig_data)
            count = 0
            while count < max_length:
                post_data = orig_data[count:count+1000]
                count+=1000
                client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                mongoDB = client['jamesbon']
                companies_col = mongoDB['companies']
                search_query = {
                    '_id':ObjectId(session['company']['id'])
                }
                company = companies_col.find_one(search_query)
                server = company['vici_server']
                user = company['vici_user']
                password = company['vici_password']
                
                url = url_builder(server, 'general_purpose_get', [])
                url += '&user='+user
                url += '&pass='+password

                ## FIND DUPLICATE PHONE NUMBERS ################################################################################
                sql_table = 'vicidial_list'
                connection = getConnection('216.244.65.82', 'cron', 'fds56FDSsdf576FSD', 'asterisk')
                sql_statement = """
                SELECT * FROM vicidial_list WHERE phone_number in (
                """
                for x in post_data:
                    phone_number = x['PHONE NUMBER'].replace('\r', '')
                    phone_number = phone_number.replace('\\r', '')
                    sql_statement += sqlescape('\'' + phone_number + '\', ')
                sql_statement = sql_statement[:-2]
                sql_statement += ') and list_id in (\''+ sqlescape(post_data[0]['list_id']) +'\');'

                client.close()

                #url += '&sql_table='+sql_table
                #url += '&sql_query='+sql_statement

                #response = requests.get(url)
                #req_data = response.text

                #data = csv_writer(req_data, ',')
                duplicate_numbers = []
                with connection:
                    with connection.cursor() as cursor:
                        ## GETTING LISTS #############################################################################################################################
                        cursor.execute(sql_statement)
                        for x in cursor:
                            duplicate_numbers.append(str(x['phone_number']))

                        ## FIND SYSTEM DNC PHONE NUMBERS ################################################################################
                        #sql_table = 'vicidial_dnc'
                        #sql_statement = """
                        #SELECT * FROM vicidial_dnc WHERE phone_number in (
                        #"""
                        #for x in post_data:
                        #    phone_number = x['PHONE NUMBER'].replace('\r', '')
                        #    phone_number = phone_number.replace('\\r', '')
                        #    sql_statement += '\'' + sqlescape(phone_number) + '\', '
                        #sql_statement = sql_statement[:-2]
                        #sql_statement += ');'
                        #
                        #url = url_builder(server, 'general_purpose_get', [])
                        #url += '&user='+user
                        #url += '&pass='+password
                        #
                        #url += '&sql_table='+sql_table
                        #url += '&sql_query='+sql_statement
                        #
                        #data = csv_writer(req_data, ',')
                        #duplicate_numbers = []
                        #for x in data:
                        #    duplicate_numbers.append(str(x['phone_number']))
                        #
                        ## INSERT PHONE NUMBERS ################################################################################

                        sql_statement = """
                        INSERT INTO vicidial_list (address1, address2, address3, alt_phone, called_count, called_since_last_reset, city, comments, country_code, date_of_birth, email, entry_date, entry_list_id, first_name, gender, gmt_offset_now, last_local_call_time, last_name, list_id, middle_initial, modify_date, owner, phone_code, phone_number, postal_code, province, rank, security_phrase, source_id, state, status, title, user, vendor_lead_code)
                        VALUES
                        """
                        insert = False
                        for x in post_data:
                            phone_number = x['PHONE NUMBER'].replace('\r', '')
                            phone_number = phone_number.replace('\\r', '')
                            if phone_number not in duplicate_numbers:
                                sql_statement += '('
                                now = datetime.datetime.now() # current date and time
                                date_time = now.strftime("%m/%d/%Y %H:%M:%S")
                                area_code = phone_number[:3]
                                #if area_code == '287' or area_code == '372' or area_code == '446' or area_code == '887' or area_code == '798':
                                #area_code = '239'
                                state = pyAreadCodes.areaCodeTZ[area_code]['state']
                                regions = pyAreadCodes.areaCodeTZ[area_code]['regions']
                                region = regions.split(',')[0]

                                try:
                                    postal_code = x['POSTAL CODE'].replace('\r', '')
                                    postal_code = postal_code.replace('\\r', '')
                                    GMT_DIF = pyPostalCodes.postalCodesTZ[postal_code]
                                except:
                                    GMT_DIF = pyAreadCodes.areaCodeTZ[area_code]['GMT_DIF']

                                try:
                                    first_name = x['FIRST NAME']
                                except:
                                    first_name = ''
                                try:
                                    last_name = x['LAST NAME']
                                except:
                                    last_name = ''
                                try:
                                    email = x['EMAIL']
                                except:
                                    email = ''
                                try:
                                    postal_code = x['POSTAL CODE'].replace('\r', '')
                                    postal_code = postal_code.replace('\\r', '')
                                except:
                                    postal_code = ''
                                try:
                                    state = x['STATE']
                                except:
                                    pass
                                try:
                                    region = x['CITY'].replace('\r', '')
                                    region = region.replace('\\r', '')
                                except:
                                    pass

                                numeric_filter = filter(str.isdigit, x['PHONE NUMBER'])
                                phone_number = "".join(numeric_filter)
                                base_value = {
                                    "address1": "", 
                                    "address2": "", 
                                    "address3": "", 
                                    "alt_phone": "", 
                                    "called_count": 0, 
                                    "called_since_last_reset": "N", 
                                    "city": region, 
                                    "comments": "", 
                                    "country_code": "1", 
                                    "date_of_birth": "0000-00-00", 
                                    "email": email, 
                                    "entry_date": date_time, 
                                    "entry_list_id": 0, 
                                    "first_name": first_name, 
                                    "gender": "", 
                                    "gmt_offset_now": str(float(GMT_DIF))+'0', 
                                    "last_local_call_time": date_time, 
                                    "last_name": last_name, 
                                    "list_id": x['list_id'], 
                                    "middle_initial": "", 
                                    "modify_date": date_time, 
                                    "owner": "", 
                                    "phone_code": 1, 
                                    "phone_number": phone_number, 
                                    "postal_code": postal_code, 
                                    "province": "", 
                                    "rank": 0, 
                                    "security_phrase": "", 
                                    "source_id": "", 
                                    "state": state, 
                                    "status": "NEW", 
                                    "title": "", 
                                    "user": "VDAD", 
                                    "vendor_lead_code": ""
                                }
                                for y in base_value:
                                    sql_statement += '\'' + sqlescape(str(base_value[y])) + '\','
                                sql_statement = sql_statement[:-1]
                                sql_statement += '),'
                                insert = True
                        sql_statement = sql_statement[:-1]
                        sql_statement += ';'
                        if insert:
                            cursor.execute(sql_statement)
                    if insert:
                        connection.commit()
                #sql_statements = []
                #sql_statements.append(sql_statement)
                #if insert:
                #    message = sql_writer(sql_statements, server, user, password)
            return  jsonify({'Message':'Success'})

@viciApiBlueprint.route('/api/vici/leads/export', methods=['GET'])
def viciGetLeadDataExport():
    if validateLogin():
        if request.method == 'GET':
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']
            ## GET LISTS FROM CAMPAIGN ######################################################################
            url = url_builder(server, 'general_purpose_get', [])
            url += '&user='+user
            url += '&pass='+password

            sql_table = 'vicidial_log'
            column_overide='list_id'
            sql_statement = """
                SELECT vls.list_id
                FROM vicidial_lists vls,vicidial_list vl 
                WHERE vls.list_id=vl.list_id and campaign_id='{}'
                GROUP BY list_id
            """.format(sqlescape(request.args.get('campaign_id')))

            url += '&column_overide='+column_overide
            url += '&sql_table='+sql_table
            url += '&sql_query='+sql_statement

            client.close()

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')
            lists = []
            for x in data:
                if x['list_id'] != '':
                    lists.append(str(x['list_id']))
            list_str = str(lists)
            list_str = list_str.replace('[', '')
            list_str = list_str.replace(']', '')

            ## GET LOGS FROM LISTS ##########################################################################
            url = url_builder(server, 'general_purpose_get', [])
            url += '&user='+user
            url += '&pass='+password

            sql_table = 'vicidial_log'
            column_overide='lead_id,campaign_id,status,phone_number,title,first_name,last_name,middle_initial,address1,address2,address3,city,state,province,postal_code,country_code,gender,date_of_birth,email,called_count,last_local_call_time,call_date,length_in_sec,status,location'
            sql_statement = """
                SELECT l.lead_id
                    ,cl.campaign_id 
                    ,l.status
                    ,l.phone_number 
                    ,l.title
                    ,l.first_name 
                    ,l.last_name 
                    ,l.middle_initial 
                    ,l.address1 
                    ,l.address2 
                    ,l.address3 
                    ,l.city
                    ,l.state
                    ,l.province 
                    ,l.postal_code 
                    ,l.country_code 
                    ,l.gender
                    ,l.date_of_birth 
                    ,l.email
                    ,l.called_count 
                    ,l.last_local_call_time 
                    ,cl.call_date 
                    ,cl.length_in_sec 
                    ,cl.status 
                    ,rl.location 
                FROM vicidial_list as l 
                LEFT JOIN vicidial_log as cl 
                ON l.lead_id = cl.lead_id and cl.campaign_id = '{}'
                LEFT JOIN recording_log rl 
                ON l.lead_id = rl.lead_id  and cl.uniqueid = rl.vicidial_id 
                WHERE l.list_id in ({})
            """.format(sqlescape(request.args.get('campaign_id')), list_str)

            url += '&column_overide='+column_overide
            url += '&sql_table='+sql_table
            url += '&sql_query='+sql_statement

            client.close()

            response = requests.get(url)
            req_data = response.text

            data = csv_writer(req_data, ',')

            formatted_data = {}
            for x in data:
                if not formatted_data.get(x['lead_id']):
                    formatted_data[x['lead_id']] = {
                        'lead_id':x['lead_id'],
                        'campaign_id':x['campaign_id'],
                        'status':x['status'],
                        'phone_number':x['phone_number'],
                        'title':x['title'],
                        'first_name':x['first_name'],
                        'last_name':x['last_name'],
                        'middle_initial':x['middle_initial'],
                        'address1':x['address1'],
                        'address2':x['address2'],
                        'address3':x['address3'],
                        'city':x['city'],
                        'state':x['state'],
                        'province':x['province'],
                        'postal_code':x['postal_code'],
                        'country_code':x['country_code'],
                        'gender':x['gender'],
                        'date_of_birth':x['date_of_birth'],
                        'email':x['email'],
                        'called_count':x['called_count'],
                        'last_local_call_time':x['last_local_call_time'],
                        'call_logs':[]
                    }
                formatted_data[x['lead_id']]['call_logs'].append({
                    'call_date':x['call_date'],
                    'length_in_sec':x['length_in_sec'],
                    'status':x['status'],
                    'location':x['location']
                })
            return_csv = [['lead_id','campaign_id','status','phone_number','title','first_name','last_name','middle_initial','address1','address2','address3','city','state','province','postal_code','country_code','gender','date_of_birth','email','called_count','last_local_call_time','call_date','length_in_sec','status','location']]
            for x in formatted_data:
                z = formatted_data[x]
                plus_csv_2 = []
                plus_csv_2.append(str(z['lead_id']))
                plus_csv_2.append(str(z['campaign_id']))
                plus_csv_2.append(str(z['status']))
                plus_csv_2.append(str(z['phone_number']))
                plus_csv_2.append(str(z['title']))
                plus_csv_2.append(str(z['first_name']))
                plus_csv_2.append(str(z['last_name']))
                plus_csv_2.append(str(z['middle_initial']))
                plus_csv_2.append(str(z['address1']))
                plus_csv_2.append(str(z['address2']))
                plus_csv_2.append(str(z['address3']))
                plus_csv_2.append(str(z['city']))
                plus_csv_2.append(str(z['state']))
                plus_csv_2.append(str(z['province']))
                plus_csv_2.append(str(z['postal_code']))
                plus_csv_2.append(str(z['country_code']))
                plus_csv_2.append(str(z['gender']))
                plus_csv_2.append(str(z['date_of_birth']))
                plus_csv_2.append(str(z['email']))
                plus_csv_2.append(str(z['called_count']))
                plus_csv_2.append(str(z['last_local_call_time']))
                print((z['call_logs']))
                print(len(z['call_logs']))
                if len(z['call_logs']) > 0:
                    plus_csv_2.append(str(z['call_logs'][0]['call_date']))
                    plus_csv_2.append(str(z['call_logs'][0]['length_in_sec']))
                    plus_csv_2.append(str(z['call_logs'][0]['status']))
                    plus_csv_2.append(str(z['call_logs'][0]['location']))
                else:
                    plus_csv_2.append('')
                    plus_csv_2.append('')
                    plus_csv_2.append('')
                    plus_csv_2.append('')
                return_csv.append(plus_csv_2)
                if len(z['call_logs']) > 1:
                    plus_csv_2 = []
                    for x in range(1, len(z['call_logs'])):
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append('')
                        plus_csv_2.append(str(z['call_logs'][x]['call_date']))
                        plus_csv_2.append(str(z['call_logs'][x]['length_in_sec']))
                        plus_csv_2.append(str(z['call_logs'][x]['status']))
                        plus_csv_2.append(str(z['call_logs'][x]['location']))
                    return_csv.append(plus_csv_2)

            return jsonify(return_csv)

@viciApiBlueprint.route('/api/vici/call_logs', methods=['GET'])
def viciGetCallLogs():
    if validateLogin():
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        companies_col = mongoDB['companies']
        search_query = {
            '_id':ObjectId(session['company']['id'])
        }
        company = companies_col.find_one(search_query)
        server = company['vici_server']
        user = company['vici_user']
        password = company['vici_password']
        
        url = url_builder(server, 'vicidial_call_logs', request.args)
        url += '&user='+user
        url += '&pass='+password
        client.close()

        response = requests.get(url)
        req_data = response.text

        data = csv_writer(req_data, ',')
        df = pd.DataFrame(data=data)
        try:
            total_seconds = df['length_in_sec'].sum()
        except:
            total_seconds = 0

        return jsonify({
            'data':data,
            'details':{
                'total_call_time':int(total_seconds)
            },
            'url':url
        })

@viciApiBlueprint.route('/api/vici/recordings', methods=['GET'])
def viciGetRecordings():
    if validateLogin():
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        companies_col = mongoDB['companies']
        search_query = {
            '_id':ObjectId(session['company']['id'])
        }
        company = companies_col.find_one(search_query)
        server = company['vici_server']
        user = company['vici_user']
        password = company['vici_password']
        
        url = url_builder(server, 'recording_logs', request.args)
        url += '&user='+user
        url += '&pass='+password
        client.close()

        response = requests.get(url)
        req_data = response.text

        data = csv_writer(req_data, ',')

        return jsonify({
            'data':data,
            'url':url
        })

@viciApiBlueprint.route('/api/vici/billing', methods=['GET'])
def viciGetBilling():
    if validateLogin():
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        companies_col = mongoDB['companies']
        search_query = {
            '_id':ObjectId(session['company']['id'])
        }
        company = companies_col.find_one(search_query)

        search_query = {
            'company_id':ObjectId(session['company']['id'])
        }
        wallet_col = mongoDB['company_wallet_balance']
        balance_row = wallet_col.find_one(search_query)
        try:
            balance = getFloatPoint(balance_row['paid_amount'])
        except:
            balance = 0


        server = company['vici_server']
        user = company['vici_user']
        password = company['vici_password']
        
        try:
            charge_per_minute = float(company['billing']['charge_amount'])
        except:
            charge_per_minute = .25
        
        url = url_builder(server, 'general_purpose_get', [])
        url += '&user='+user
        url += '&pass='+password

        sql_table = 'vicidial_log'
        column_overide='lead_id,total_seconds,campaign_id,call_date,phone_number'
        sql_statement = """
        SELECT lead_id, length_in_sec, campaign_id, call_date, phone_number FROM vicidial_log WHERE length_in_sec > 3 and call_date > '2021-11-10'
        """

        if request.args.get('campaign_id'):
            sql_statement += ' AND campaign_id = \'{}\''.format(sqlescape(request.args.get('campaign_id')))

        url += '&column_overide='+column_overide
        url += '&sql_table='+sql_table
        url += '&sql_query='+sql_statement

        client.close()

        response = requests.get(url)
        req_data = response.text

        data = csv_writer(req_data, ',')
        total_minutes = 0
        index = 0
        for x in data:
            try:
                minutes = math.ceil(int(x['total_seconds'])/60)
            except:
                minutes = 0
            total_minutes += minutes
            data[index]['type'] = 'charged'
            data[index]['rounded_minutes'] = minutes
            data[index]['total_charge'] = getFloatPoint(minutes*charge_per_minute)
            index += 1

        total_charge = total_minutes*charge_per_minute

        search_query = {
            'company_id':ObjectId(session['company']['id'])
        }
        wallet_col = mongoDB['wallet_transactions']
        balance_rows = wallet_col.find(search_query)
        for x in balance_rows:
            new_dict = {
                "call_date": x['created_at'], 
                "call_date_full": x['created_at'], 
                "memo": x['memo'], 
                "campaign_id": "", 
                "rounded_minutes": 0, 
                "phone_number":"",
                "lead_id":"CREDIT",
                "total_charge": getFloatPoint(x['amount']), 
                "total_seconds": 0,
                "type":"paid"
            }
            data.append(new_dict)

        return jsonify({
            'balance':getFloatPoint(balance),
            'total_minutes':getFloatPoint(total_minutes),
            'total_charge':getFloatPoint(total_charge),
            'remaining_balance':getFloatPoint(balance-total_charge),
            'data':data,
            'url':url
        })

@viciApiBlueprint.route('/api/vici/general', methods=['GET'])
def viciGeneralPurpose():
    if validateLogin():
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        companies_col = mongoDB['companies']
        search_query = {
            '_id':ObjectId(session['company']['id'])
        }
        company = companies_col.find_one(search_query)
        server = company['vici_server']
        user = company['vici_user']
        password = company['vici_password']
        
        url = url_builder(server, 'general_purpose_get', [])
        url += '&user='+user
        url += '&pass='+password

        sql_table = 'vicidial_live_agents'
        #column_overide='status,number_of_lines'
        sql_statement = """
        SELECT * FROM vicidial_live_agents
        """

        #url += '&column_overide='+column_overide
        url += '&sql_table='+sql_table
        url += '&sql_query='+sql_statement

        client.close()

        response = requests.get(url)
        req_data = response.text

        data = csv_writer(req_data, ',')

        #return_data = {}
        #for x in data:
        #    return_data[x['postal_code']] = x['GMT_offset']

        return jsonify(data)
        #return jsonify({
        #    'data':data,
        #    'url':url
        #})

@viciApiBlueprint.route('/api/vici/gen_campaigns', methods=['GET'])
def viciGetGenCampaigns():
    if validateLogin():
        if request.method == 'GET':        
            client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            mongoDB = client['jamesbon']
            companies_col = mongoDB['companies']
            search_query = {
                '_id':ObjectId(session['company']['id'])
            }
            company = companies_col.find_one(search_query)
            server = company['vici_server']
            user = company['vici_user']
            password = company['vici_password']

            campaign_list = getAllCampaigns(session['company']['id'], 'str')

            client.close()
            
            url = url_builder_new(server, 'campaigns_get', [])
            url += '&campaign_list='+campaign_list
            url += '&user='+user
            url += '&pass='+password

            response = requests.get(url)
            req_data = response.text

            data = csv_writer_multi(req_data, ',')

            return_data = {}
            for x in data[0]:
                if not return_data.get(x['campaign_id']):
                    status = 'STOPPED'
                    if x['status'] == 'ACTIVE':
                        status = 'RUNNING'
                    return_data[x['campaign_id']] = {
                        "call_count":0,
                        "lead_count":0,
                        "remaining_leads":0,
                        "number_of_lines":x['number_of_lines'],
                        "status":status
                    }
                    return_data[x['campaign_id']]['lists'] = []
                list_obj = x
                list_obj['call_count'] = float(x['call_count'])
                return_data[x['campaign_id']]['lists'].append(x)
                return_data[x['campaign_id']]['call_count'] += float(x['call_count'])
                return_data[x['campaign_id']]['lead_count'] += float(x['tally'])
                return_data[x['campaign_id']]['remaining_leads'] = float(return_data[x['campaign_id']]['lead_count'] - return_data[x['campaign_id']]['call_count'])

            return_data_full = []
            for row in data[1]:
                dict_obj = {}
                for col in row:
                    dict_obj[col] = row[col]
                return_data_full.append(dict_obj)

            for x in range(0, len(return_data_full)):
                try:
                    return_data_full[x]['extra_detail'] = return_data[return_data_full[x]['campaign_id']]
                    return_data_full[x]['number_of_lines'] = return_data[return_data_full[x]['campaign_id']]['number_of_lines']
                except:
                    return_data_full[x]['extra_detail'] = {}

            return jsonify({
                'data':return_data_full,
                'url':url
            })

def viciGetBillingToday(today_date):
    if validateLogin():
        client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongoDB = client['jamesbon']
        companies_col = mongoDB['companies']
        search_query = {
            '_id':ObjectId(session['company']['id'])
        }
        company = companies_col.find_one(search_query)

        search_query = {
            'company_id':ObjectId(session['company']['id'])
        }
        wallet_col = mongoDB['company_wallet_balance']
        balance_row = wallet_col.find_one(search_query)
        try:
            balance = getFloatPoint(balance_row['paid_amount'])
        except:
            balance = 0


        server = company['vici_server']
        user = company['vici_user']
        password = company['vici_password']
        
        url = url_builder(server, 'general_purpose_get', [])
        url += '&user='+user
        url += '&pass='+password
        
        try:
            charge_per_minute = float(company['billing']['charge_amount'])
        except:
            charge_per_minute = .25

        list_list = getAllLists(session['company']['id'], 'str')

        sql_table = 'vicidial_log'
        column_overide='lead_id,total_seconds,campaign_id,call_date,phone_number'
        sql_statement = """
        SELECT lead_id, length_in_sec, campaign_id, call_date, phone_number FROM vicidial_log WHERE length_in_sec > 3 and call_date > '{}' and list_id in ({})
        """.format(sqlescape(today_date), list_list)

        url += '&column_overide='+column_overide
        url += '&sql_table='+sql_table
        url += '&sql_query='+sql_statement

        client.close()

        response = requests.get(url)
        req_data = response.text

        data = csv_writer(req_data, ',')
        total_minutes = 0
        campaign_minute_breakdown = {}
        index = 0
        for x in data:
            try:
                minutes = math.ceil(int(x['total_seconds'])/60)
            except:
                minutes = 0
            total_minutes += minutes
            data[index]['type'] = 'charged'
            data[index]['rounded_minutes'] = minutes
            data[index]['total_charge'] = getFloatPoint(minutes*charge_per_minute)
            if not campaign_minute_breakdown.get(x['campaign_id']):
                campaign_minute_breakdown[x['campaign_id']] = {
                    'rounded_minutes':0,
                    'total_charge':0
                }
            campaign_minute_breakdown[x['campaign_id']]['rounded_minutes'] += minutes
            campaign_minute_breakdown[x['campaign_id']]['total_charge'] = campaign_minute_breakdown[x['campaign_id']]['rounded_minutes']*charge_per_minute
            index += 1

        total_charge = total_minutes*charge_per_minute

        search_query = {
            'company_id':ObjectId(session['company']['id'])
        }
        wallet_col = mongoDB['wallet_transactions']
        balance_rows = wallet_col.find(search_query)
        for x in balance_rows:
            new_dict = {
                "call_date": x['created_at'], 
                "call_date_full": x['created_at'], 
                "memo": x['memo'], 
                "campaign_id": "", 
                "rounded_minutes": 0, 
                "phone_number":"",
                "lead_id":"CREDIT",
                "total_charge": getFloatPoint(x['amount']), 
                "total_seconds": 0,
                "type":"paid"
            }
            data.append(new_dict)

        campaign_minute_breakdown_list = []
        for x in campaign_minute_breakdown:
            dict_new = campaign_minute_breakdown[x]
            dict_new['campaign_id'] = x
            campaign_minute_breakdown_list.append(dict_new)

        billing_dict = {
            'charge_amount':getFloatPoint(balance)-getFloatPoint(total_charge),
            'campaign_minute_breakdown':campaign_minute_breakdown_list
        }
        return billing_dict


def getFloatPoint(a):
    try:
        x = float("{:.2f}".format(round(a, 2)))
    except:
        x = float("{:.2f}".format(round(0, 2)))
    return x

def getAllCampaigns(company_id, type_return):
    client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mongoDB = client['jamesbon']
    campaign_members = mongoDB['campaign_members_new']
    search_query = {
        'company_id':str(company_id)
    }

    campaign_list = []
    for member in campaign_members.find(search_query):
        campaign_list.append(str(member['campaign_id']))
    if type_return == 'list':
        return campaign_list
    else:
        campaign_list_str = str(campaign_list)
        campaign_list_str = str(campaign_list_str).replace('[','')
        campaign_list_str = str(campaign_list_str).replace(']','')
        return campaign_list_str

def getAllLists(company_id,type_return):
    client = pymongo.MongoClient("mongodb+srv://admin:QM6icvpQ6SlOveul@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mongoDB = client['jamesbon']
    campaign_members = mongoDB['list_members']
    search_query = {
        'company_id':str(company_id)
    }

    list_list = []
    for member in campaign_members.find(search_query):
        list_list.append(str(member['list_id']))
    if type_return == 'list':
        return list_list
    else:
        list_list_str = str(list_list)
        list_list_str = str(list_list_str).replace('[','')
        list_list_str = str(list_list_str).replace(']','')
        if list_list_str == '':
            list_list_str = 'NULL'
        return list_list_str

def getGMTOffset(postal_code, connection):
    query = '''
    SELECT GMT_offset
    FROM vicidial_postal_codes
    WHERE postal_code = '{}'
    '''.format(sqlescape(postal_code))
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for x in cursor:
                return x['GMT_offset']
    return None

def getInt(x):
    try:
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)
    except:
        x = 0
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)