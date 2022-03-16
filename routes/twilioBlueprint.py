from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *
import config

twilioBlueprint = Blueprint('twilioAPI', __name__)

@twilioBlueprint.route('/api/v1/twilio/profiles', methods=['GET', 'POST'])
def profilesAPI():
    if True:
        if request.method == 'GET':
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            twilio_settings_col = mongoDB['companies']

            filterBy = {}

            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    filterBy['_id'] = ObjectId(request.args.get('companyid'))
                else:
                    return jsonify({'Message':'Failure'})
            else:
                try:
                    if session['user']['company_id']:
                        filterBy['_id'] = ObjectId(session['user']['company_id'])
                    else:
                        return jsonify({'Message':'Failure'})
                except:
                    #client.close()
                    return jsonify({'Message':'Failure'})

            company_twilio_settings = twilio_settings_col.find_one(filterBy)
            twilio_account_sid = company_twilio_settings['twilio_account_sid']
            twilio_auth_token = company_twilio_settings['twilio_auth_token']
            twilio_profile_sid = company_twilio_settings['twilio_profile_sid']

            return_post = []

            twilClient = Client(twilio_account_sid, twilio_auth_token)
            trust_products = twilClient.trusthub.customer_profiles.list(limit=20)
            for trust_product in trust_products:
                return_post.append(trust_product.__dict__['_properties'])
            return jsonify(return_post)

    return jsonify({'Message':'Failure'})

@twilioBlueprint.route('/api/v1/twilio/profiles/phones', methods=['GET'])
def profilesPhonesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        twilio_settings_col = mongoDB['companies']

        filterBy = {}

        if request.args.get('companyid'):
            if validateCompany(request.args.get('companyid')):
                filterBy['_id'] = ObjectId(request.args.get('companyid'))
            else:
                return jsonify({'Message':'Failure'})
        else:
            try:
                if session['user']['company_id']:
                    filterBy['_id'] = ObjectId(session['user']['company_id'])
                else:
                    return jsonify({'Message':'Failure'})
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

        company_twilio_settings = twilio_settings_col.find_one(filterBy)
        twilio_account_sid = company_twilio_settings['twilio_account_sid']
        twilio_auth_token = company_twilio_settings['twilio_auth_token']

        twilio_profile_sid = None
        if request.args.get('profileid'):
            twilio_profile_sid = request.args.get('profileid')
        else:
            return jsonify({'Message':'Failure'})

        return_post = []

        twilClient = Client(twilio_account_sid, twilio_auth_token)
        trust_products = twilClient.trusthub.customer_profiles(twilio_profile_sid) \
        .customer_profiles_channel_endpoint_assignment.list(limit=20)
        for trust_product in trust_products:
            try:
                a = trust_product.__dict__['_properties']
                number = twilClient.incoming_phone_numbers(a['channel_endpoint_sid']).fetch()
                a['phone_number'] = number.__dict__['_properties']['phone_number']
                return_post.append(a)
            except:
                pass
        return jsonify(return_post)

@twilioBlueprint.route('/api/v1/twilio/shakenstirs', methods=['GET'])
def trustedProductsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        twilio_settings_col = mongoDB['companies']

        filterBy = {}

        if request.args.get('companyid'):
            if validateCompany(request.args.get('companyid')):
                filterBy['_id'] = ObjectId(request.args.get('companyid'))
            else:
                return jsonify({'Message':'Failure'})
        else:
            try:
                if session['user']['company_id']:
                    filterBy['_id'] = ObjectId(session['user']['company_id'])
                else:
                    return jsonify({'Message':'Failure'})
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

        company_twilio_settings = twilio_settings_col.find_one(filterBy)
        twilio_account_sid = company_twilio_settings['twilio_account_sid']
        twilio_auth_token = company_twilio_settings['twilio_auth_token']
        twilio_profile_sid = company_twilio_settings['twilio_profile_sid']

        return_post = []

        twilClient = Client(twilio_account_sid, twilio_auth_token)
        trust_products = twilClient.trusthub.trust_products.list(limit=20)

        for trust_product in trust_products:
            return_post.append(trust_product.__dict__['_properties'])
        return jsonify(return_post)

@twilioBlueprint.route('/api/v1/twilio/shakenstirs/phones', methods=['GET'])
def trustedProductsPhonesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        twilio_settings_col = mongoDB['companies']

        filterBy = {}

        if request.args.get('companyid'):
            if validateCompany(request.args.get('companyid')):
                filterBy['_id'] = ObjectId(request.args.get('companyid'))
            else:
                return jsonify({'Message':'Failure'})
        else:
            try:
                if session['user']['company_id']:
                    filterBy['_id'] = ObjectId(session['user']['company_id'])
                else:
                    return jsonify({'Message':'Failure'})
            except:
                #client.close()
                return jsonify({'Message':'Failure'})


        company_twilio_settings = twilio_settings_col.find_one(filterBy)
        twilio_account_sid = company_twilio_settings['twilio_account_sid']
        twilio_auth_token = company_twilio_settings['twilio_auth_token']

        twilio_profile_sid = None
        if request.args.get('profileid'):
            twilio_profile_sid = request.args.get('profileid')
        else:
            return jsonify({'Message':'Failure'})

        return_post = []

        twilClient = Client(twilio_account_sid, twilio_auth_token)
        trust_products = twilClient.trusthub.trust_products(twilio_profile_sid).trust_products_channel_endpoint_assignment.list()
        for trust_product in trust_products:
            try:
                a = trust_product.__dict__['_properties']
                number = twilClient.incoming_phone_numbers(a['channel_endpoint_sid']).fetch()
                a['phone_number'] = number.__dict__['_properties']['phone_number']
                return_post.append(a)
            except:
                pass
        return jsonify(return_post)