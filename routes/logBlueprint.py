
from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from customerAPI import convertToJSON

from univFuncs import *

logBlueprint = Blueprint('logAPI', __name__)

@logBlueprint.route('/api/v1/users/all', methods=['GET'])
def apiUsersAll():
    if validateLogin():
        if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
            jamesbonDB = app.mongo_client['jamesbon']
            logDB = app.mongo_client['logs']
            users_col = jamesbonDB['users']
            if request.method == 'GET':
                return_post = []
                for user in users_col.find().sort("email"):
                    return_post.append({
                        'id':str(user['_id']),
                        'first_name':user['first_name'],
                        'last_name':user['last_name'],
                        'email':user['email']
                    })
                return jsonify(return_post)
    return jsonify({'Message':'Failure'})

@logBlueprint.route('/api/v1/ip_addr', methods=['GET'])
def apiGetIPAddr():
    remote_ip = str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(',')
    return jsonify({'ip': remote_ip[0]})

@logBlueprint.route('/api/v1/users/logs', methods=['GET'])
def apiUserLogs():
    if validateLogin():
        if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
            jamesbonDB = app.mongo_client['jamesbon']
            logDB = app.mongo_client['logs']
            users_col = jamesbonDB['users']
            users_log_col = logDB['users']
            collection_log_col = logDB['collections']
            if request.method == 'GET':
                return_post = []
                user_dict = {}
                for user in users_col.find():
                    user_dict[str(user['_id'])] = {
                        'first_name':user['first_name'],
                        'last_name':user['last_name'],
                        'email':user['email']
                    }

                filterBy = {}
                if request.args.get('logid'):
                    filterBy['_id'] = ObjectId(request.args.get('logid'))

                if request.args.get('userid'):
                    filterBy['user_id'] = ObjectId(request.args.get('userid'))

                if request.args.get('from') and request.args.get('to'):
                    filterBy['created_at'] = {
                        "$gte":request.args.get('from'),
                        "$lte":request.args.get('to')
                    }
                elif request.args.get('from'):
                    filterBy['created_at'] = {
                        "$gte":request.args.get('from')
                    }
                elif request.args.get('to'):
                    filterBy['created_at'] = {
                        "$lte":request.args.get('to')
                    }

                print(filterBy)

                for user in users_log_col.find(filterBy).sort("created_at"):
                    try:
                        a = {
                            'id':str(user['_id']),
                            'location':str(user['location']),
                            'action':'GET',
                            'created_at':user['created_at'],
                            'first_name':user_dict[str(user['user_id'])]['first_name'],
                            'last_name':user_dict[str(user['user_id'])]['last_name'],
                            'email':user_dict[str(user['user_id'])]['email']
                        }
                        try:
                            a['company_id'] = str(user['company_id'])
                        except:
                            pass
                        try:
                            a['ip'] = str(user['ip'])
                        except:
                            pass
                        return_post.append(a)
                    except:
                        pass

                for user in collection_log_col.find(filterBy).sort("created_at"):
                    try:
                        a = {
                            'id':str(user['_id']),
                            'location':str(user['collection']),
                            'action':user['type'],
                            'created_at':user['created_at'],
                            'first_name':user_dict[str(user['user_id'])]['first_name'],
                            'last_name':user_dict[str(user['user_id'])]['last_name'],
                            'email':user_dict[str(user['user_id'])]['email']
                        }
                        try:
                            a['company_id'] = str(user['company_id'])
                        except:
                            pass
                        try:
                            a['ip'] = str(user['ip'])
                        except:
                            pass
                        if request.args.get('logid'):
                            a['query'] = convertToJSON(user['query'])
                        return_post.append(a)
                    except:
                        pass

                return jsonify(return_post)
    return jsonify({'Message':'Failure'})