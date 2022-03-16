from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *
import config

import plivo

plivoBlueprint = Blueprint('plivoAPI', __name__)

@plivoBlueprint.route('/api/v1/plivo/make_call', methods=['GET', 'POST'])
def makeCallAPI():
    client = plivo.RestClient('MAYMUWNWQYYTA4MZCYYW','OTFmYjk2YzBjMTM3MzczM2M4OTVmZDg2MDllOTZh')
    response = client.calls.create(
        from_='+18337600738',
        to_='+12392208726',
        answer_url='https://a7dc-12-206-86-26.ngrok.io/plivo/call_back',
        answer_method='POST', )
    print(response)
    return Response(str(response), mimetype="text/xml")

@plivoBlueprint.route('/api/v1/plivo/call_status', methods=['GET', 'POST'])
def callStatusAPI():
    try:
        print(request.form)
    except:
        pass
    try:
        print(request.json)
    except:
        pass
    response = '''<Response> 
        <GetInput action="https://3814-12-206-86-26.ngrok.io/api/v1/plivo/call_status" inputType="speech"> 
            <Play>https://obama-care.s3.amazonaws.com/u65/rephrase.mp3</Play> 
        </GetInput> 
    </Response>'''
    return Response(response, mimetype='application/xml')

@plivoBlueprint.route('/api/v1/plivo/call_hangup', methods=['GET', 'POST'])
def callHangupAPI():
    try:
        print(request.form)
    except:
        pass
    try:
        print(request.json)
    except:
        pass
    return 'success'

@plivoBlueprint.route('/api/v1/plivo/call_fallback', methods=['GET', 'POST'])
def callFallbackAPI():
    try:
        print(request.form)
    except:
        pass
    try:
        print(request.json)
    except:
        pass
    return 'success'