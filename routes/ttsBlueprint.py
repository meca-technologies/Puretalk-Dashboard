from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from flask.templating import render_template
from itsdangerous import exc
from pendulum import date
from werkzeug.utils import redirect
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *
import config
import bcrypt

# TTS CONVERT LIBRARIES
import os
import hashlib

# SQUARE STUFF
import uuid
from square.client import Client

ttsBlueprint = Blueprint('ttsAPI', __name__)

def validateTTSLogin():
    try:
        if session['tts']:
            mongoDB = app.mongo_client['stt-db']
            users_col = mongoDB['users']
            search_query = {
                '_id':ObjectId(session['tts']['user']['_id']),
                'logins':session['tts']['login_session']
            }
            user = users_col.find_one(search_query)
            if user:
                for key in session['tts']['login_session']:
                    expire_str = user['logins'][key]['expires']
                    curr_time = datetime.datetime.utcnow()
                    expire_date = datetime.datetime.strptime(expire_str, '%Y-%m-%d %H:%M:%S.%f')
                    if curr_time > expire_date:
                        return False
                return True
            return False
        else:
            return False
    except:
        return False

@ttsBlueprint.route('/tts/', methods=['GET', 'POST'])
def ttsIndex():
    if request.method == 'GET':
        if validateTTSLogin():
            mongoDB = app.mongo_client['stt-db']
            users_col = mongoDB['users']
            search_query = {
                '_id':ObjectId(session['tts']['user']['_id'])
            }
            user = users_col.find_one(search_query)

            projects = user['projects']
            for x in range(0, len(projects)):
                projects[x]['project_number'] = str(projects[x]['project_number'])

            login_session = session['tts']['login_session']
            session['tts'] = {
                'user':{
                    'first_name':user['first_name'],
                    'last_name':user['last_name'],
                    'company':user['company'],
                    'auth_token':user['auth_token'],
                    'interest':user['interest'],
                    'email':user['email'],
                    '_id':str(user['_id']),
                },
                'companies':[{
                    'account_number':str(session['tts']['user']['_id']),
                    'auth_token':str(user['auth_token']),
                    'name':str(user['company'])
                }],
                'projects':projects,
                'login_session':login_session
            }
            return render_template('tts-dashboard/index.html', companyName='PureTalk', pageTitle='Dashboard', navPosition='index')
        else:
            return redirect('/tts/logout')
    if request.method == 'POST':
        session.clear()
        mongoDB = app.mongo_client['stt-db']
        users_col = mongoDB['users']
        email = request.form['email']
        password = bytes(request.form['password'], 'utf-8')

        search_query = {
            'email':email
        }
        user = users_col.find_one(search_query)
        if bcrypt.checkpw(password,bytes(user['password'], 'utf-8')):
            insert_data = {
                'first_name':user['first_name'],
                'last_name':user['last_name'],
                'company':user['company'],
                'auth_token':str(user['auth_token']),
                'interest':user['interest'],
                'email':user['email'],
                'projects':user['projects']
            }
            insert_data['auth_token'] = str(insert_data['auth_token'])
            insert_data['_id'] = str(user['_id'])
            
            projects = insert_data['projects']
            for x in range(0, len(projects)):
                projects[x]['project_number'] = str(projects[x]['project_number'])
            login_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)

            login_session_id = str(ObjectId())
            login_session = {
                'expires':str(login_time),
                'ip':(str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))[0]
            }
            session['tts'] = {
                'user':insert_data,
                'companies':[{
                    'account_number':str(user['_id']),
                    'auth_token':str(user['auth_token']),
                    'name':str(user['company'])
                }],
                'projects':projects,
                'login_session':{
                    login_session_id:login_session
                }
            }
            
            search_query = {
                '_id':user['_id']
            }
            update_query = {
                '$set':{
                    'logins.'+login_session_id:login_session
                }
            }
            users_col.update_one(search_query, update_query)
            return redirect('/tts/')
        return redirect('/tts/signup?location=login-details')
            
@ttsBlueprint.route('/tts/signup', methods=['GET', 'POST'])
def ttsSignUp():
    if request.method == 'GET':
        try:
            error_message = session['tts']['error']
        except:
            error_message = None
        session.clear()
        return render_template('tts-dashboard/signup.html', companyName='PureTalk', pageTitle='Dashboard', navPosition='index', error_message=error_message)
    elif request.method == 'POST':
        if not validateTTSLogin():
            mongoDB = app.mongo_client['stt-db']
            users_col = mongoDB['users']
            password_raw = bytes(request.form.get('password'), 'utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_raw, salt)
            password = str(hashed)[2:-1]

            search_query = {
                'email':request.form.get('email')
            }
            if not users_col.find_one(search_query):
                auth_token = ObjectId()
                login_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                login_session = {
                    str(ObjectId()):{
                        'expires':str(login_time),
                        'ip':(str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))[0]
                    }
                }
                insert_data = {
                    'first_name':request.form.get('first-name'),
                    'last_name':request.form.get('last-name'),
                    'company':request.form.get('company'),
                    'auth_token':str(auth_token),
                    'interest':request.form.get('interest'),
                    'email':request.form.get('email'),
                    'password':password,
                    'projects':[],
                    'logins':[],
                    'square_details':{}
                }
                insert_data['logins'].append(login_session)
                _id = users_col.insert(insert_data)
                insert_data['auth_token'] = str(insert_data['auth_token'])
                insert_data['_id'] = str(_id)
                insert_data.pop('password')
                insert_data.pop('logins')
                session['tts'] = {
                    'user':insert_data,
                    'companies':[{
                        'account_number':str(_id),
                        'auth_token':str(auth_token),
                        'name':str(request.form.get('company'))
                    }],
                    'projects':insert_data['projects']
                }
                return redirect('/tts/')
        session['tts'] = {
            'error':'Incorrect Email'
        }
        return redirect('/tts/signup?location=sign-up-details')
        
@ttsBlueprint.route('/tts/logout', methods=['GET', 'POST'])
def ttsLogout():
    mongoDB = app.mongo_client['stt-db']
    users_col = mongoDB['users']
    try:
        search_query = {
            '_id':ObjectId(session['tts']['user']['_id'])
        }
        login_key = None
        for key in session['tts']['login_session']:
            login_key = key
        update_query = {
            '$unset': {
                'logins':login_key
            }
        }
        users_col.update_one(search_query, update_query)
    except:
        pass
    session.clear()
    return redirect('/tts/signup?location=login-details')

@ttsBlueprint.route('/api/v1/tts/companies', methods=['GET', 'POST'])
def companiesAPI():
    print('Hello')

@ttsBlueprint.route('/api/v1/tts/projects', methods=['POST', 'PUT', 'DELETE'])
def projectsAPI():
    mongoDB = app.mongo_client['stt-db']
    users_col = mongoDB['users']
    if request.method == 'POST':
        post_data = request.json
        search_query = {
            '_id':ObjectId(session['tts']['user']['_id'])
        }

        project_id = ObjectId()
        insert_query = {
            '$push':{
                'projects':{
                    'name':post_data['name'],
                    'project_number':project_id,
                    'account_number':session['tts']['user']['_id']
                }
            }
        }
        users_col.update_one(search_query, insert_query)
        return jsonify({'Message':'Success', 'data':{
            'name':post_data['name'],
            'project_number':str(project_id),
            'account_number':session['tts']['user']['_id']
        }})
    elif request.method == 'PUT':
        update_data = request.json
        search_query = {
            'projects.project_number':ObjectId(update_data['project_number'])
        }
        update_query = {
            '$set':{
                'projects.$.name':update_data['name']
            }
        }
        users_col.update_one(search_query, update_query)
        user = users_col.find_one(search_query)
        projects = user['projects']
        for x in range(0, len(projects)):
            projects[x]['project_number'] = str(projects[x]['project_number'])

        return jsonify({'Message':'Success', 'data':projects})
    elif request.method == 'DELETE':
        update_data = request.json
        search_query = {
            'projects.project_number':ObjectId(update_data['project_number'])
        }
        update_query = {
            '$pull':{
                'projects':{
                    'project_number':ObjectId(update_data['project_number'])
                }
            }
        }
        user = users_col.find_one(search_query)
        users_col.update_one(search_query, update_query)
        user = users_col.find_one({'_id':user['_id']})
        projects = user['projects']
        for x in range(0, len(projects)):
            projects[x]['project_number'] = str(projects[x]['project_number'])

        return jsonify({'Message':'Success', 'data':projects})

@ttsBlueprint.route('/api/v1/tts/usage')
def usageAPI():
    mongoDB = app.mongo_client['stt-db']
    usage_summary_daily_col = mongoDB['usage_summary_daily']
    search_query = {
        'account_id':ObjectId(session['tts']['user']['_id'])
    }

    return_post = []
    for row in usage_summary_daily_col.find(search_query):
        return_post.append({
            'entry_date':row['entry_date'],
            'account_id':str(row['account_id']),
            'project_number':str(row['project_number']),
            'api_hits':row['api_hits'],
            'content_length':row['content_length']
        })
    return jsonify(return_post)

@ttsBlueprint.route('/api/v1/tts/<account>/convert', methods=['POST'])
def convertAPI(account):
    mongoDB = app.mongo_client['stt-db']
    users_col = mongoDB['users']

    auth_token = request.json['auth']
    if not auth_token:
        return jsonify({'Error':'No Auth Token Provided'})
    project_id = request.json['project']
    if not auth_token:
        return jsonify({'Error':'No Project ID Provided'})
    content = request.json['text']
    if not auth_token:
        return jsonify({'Error':'No Text Provided'})

    try:
        search_query = {
            '_id':ObjectId(account),
            'auth_token':auth_token,
            'projects.project_number':ObjectId(project_id)
        }
    except:
        return jsonify({'Error':'Could not authenticate!'})

    user_account = users_col.find_one(search_query)
    if user_account:
        if len(content) <= 280:
            usage_col = mongoDB['usage']
            usage_insert = {
                'account_id':ObjectId(account),
                'project_number':ObjectId(project_id),
                'content':content,
                'content_length':len(content),
                'request_type':'json',
                'created_at':str(datetime.datetime.utcnow())[:-7]
            }
            if request.headers.get('Accept') == 'audio/wave':
                usage_insert['request_type'] = 'audio'
                usage_col.insert(usage_insert)
                return Response(getTTS(content, True), mimetype="audio/wav")
            usage_col.insert(usage_insert)
            return jsonify({'audio':getTTS(content)})
        return jsonify({'Error':'Content is to long. Keep content to under 280 characters'})
    return jsonify({'Error':'Could not authenticate!'})

def getTTS(text, audio_style=False):
    url = 'http://137.184.57.49:5006/convert'
    content = text
    if audio_style:
        payload = {
            "region":"eastus",
            "text":content
        }
        req = requests.post(url, json=payload)
        return req.content
    else:
        file_name = str(hashlib.md5(content.encode('utf-8')).hexdigest()) + '.wav'
        if not findFile('./static/audio/'+file_name):
            payload = {
                "region":"eastus",
                "text":content
            }
            req = requests.post(url, json=payload)
            with open('./static/audio/'+file_name, mode='bx') as f:
                f.write(req.content)
        return './static/audio/'+file_name

def findFile(name):
    return os.path.exists(name)

@ttsBlueprint.route('/api/v1/square/customer', methods=['POST'])
def squareCustomerAPI():
    try:
        if validateTTSLogin():
            post_data = request.json
            mongoDB = app.mongo_client['stt-db']
            users_col = mongoDB['users']
            search_query = {
                '_id':ObjectId(session['tts']['user']['_id'])
            }
            cust_idempotency = str(uuid.uuid4())
            client = Client(
                access_token=config.SQUARE_ACCESS_TOKEN,
                environment='sandbox',
            )
            customer_result = client.customers.create_customer(
                body = {
                    "idempotency_key": cust_idempotency,
                    "given_name": post_data['first_name'],
                    "family_name": post_data['last_name'],
                    "company_name": post_data['company_name'],
                    "nickname": post_data['nickname'],
                    "email_address": post_data['email_address'],
                    "phone_number": post_data['phone_number'],
                    "note": ""
                }
            )
            customer_id = customer_result.body['customer']['id']
            update_query = {
                '$set':{
                    'square_details.customer_id':customer_id
                }
            }
            users_col.update_one(search_query, update_query)
            return jsonify({'Message':'Success', 'Details':{'customer_id':customer_id}})
    except:
        return jsonify({'Message':'Error'})

@ttsBlueprint.route('/api/v1/square/cards', methods=['POST'])
def squareCardsAPI():
    post_data = request.json
    mongoDB = app.mongo_client['stt-db']
    users_col = mongoDB['users']
    search_query = {
        '_id':ObjectId(post_data['account_id'])
    }
    card_idempotency = str(uuid.uuid4())
    client = Client(
        access_token=config.SQUARE_ACCESS_TOKEN,
        environment='production',
    )
    result = client.cards.create_card(
        body = {
            "idempotency_key": card_idempotency,
            "source_id": "EXTERNAL",
            "card": {
                "exp_month": post_data['exp_month'],
                "exp_year": post_data['exp_year'],
                "cardholder_name": post_data['cardholder_name'],
                "billing_address": {
                    "address_line_1": post_data['address_line_1'],
                    "postal_code": post_data['postal_code'],
                    "country": post_data['country']
                },
                "customer_id": post_data['customer_id']
            }
        }
    )