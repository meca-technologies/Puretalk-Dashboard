from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *
import config

conversationBlueprint = Blueprint('conversationAPI', __name__)

@conversationBlueprint.route('/api/v1/j2y', methods=['GET', 'POST', 'PUT', 'DELETE'])
def jToYAPI():
    data = {
        'q':str(request.json).replace("'", '"')
    }
    print(data)
    r = requests.post('https://www.json2yaml.com/api/j2y', data=data)
    try:
        print(r.text)
        print('JSON')
    except:
        pass
    return jsonify({'Message':'Success'})

@conversationBlueprint.route('/api/v1/flows', methods=['GET', 'POST', 'PUT', 'DELETE'])
def flowsAPI():
    if validateLogin():
        mongoDB = app.mongo_client['conversation-flow']
        flows_col = mongoDB['flows']
        if request.method == 'GET':
            filterBy = {}
            if request.args.get('flowid'):
                filterBy['_id'] = ObjectId(request.args.get('flowid'))

            returnPost = []

            for flow in flows_col.find(filterBy):
                flowData = convertToJSON(flow)
                returnPost.append(flowData)
            
            #client.close()
            return jsonify(returnPost)
        else:
            returnData = simpleUpdateRow(flows_col, request.json, request.method, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return jsonify({'Message':'Success'})