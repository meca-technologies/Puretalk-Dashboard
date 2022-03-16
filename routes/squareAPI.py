from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *
import config
import uuid

from square.client import Client
import stripe

squareBlueprint = Blueprint('squareAPI', __name__)

STRIPE_ACCESS_TOKEN = 'EAAAEBn_K2QBKzBQqjB3-XL2haWsArbenp2FsdlAVEgVCwK3WAhWKI9eh1E_wnwg'

@squareBlueprint.route('/api/v1/square/charge', methods=['POST'])
def squareChargeAPI():
    post_data = request.json
    mongoDB = app.mongo_client['jamesbon']
    companies_col = mongoDB['companies']
    transactions = mongoDB['wallet_transactions']
    search_query = {
        '_id':ObjectId(post_data['company_id'])
    }
    company = companies_col.find_one(search_query)
    client = Client(
        access_token=STRIPE_ACCESS_TOKEN,
        environment='sandbox',
    )
    try:
        customer_id = company['square_cust_id']
    except:
        cust_id = str(uuid.uuid4())
        customer_result = client.customers.create_customer(
            body = {
                "idempotency_key": cust_id,
                "given_name": "Shawn",
                "family_name": "Hasten",
                "company_name": "Meca Technologies",
                "nickname": "Shawn Hasten",
                "email_address": "shawn@puretalk.ai",
                "phone_number": "2392208726",
                "note": "1 South Orange Ave"
            }
        )
        customer_id = customer_result.body['customer']['id']
        update_query = {
            '$set':{
                'square_cust_id':customer_id
            }
        }
        companies_col.update_one(search_query, update_query)

    pay_id = str(uuid.uuid4())
    pay_result = client.payments.create_payment(
        body = {
            "source_id": post_data['sourceId'],
            "idempotency_key": pay_id,
            "amount_money": {
            "amount": float(post_data['amount'])*100,
            "currency": "USD"
            }
        }
    )
    

    if pay_result.body['payment']['status'] == 'COMPLETED':
        updateData = {
            'company_id':ObjectId(post_data['company_id']),
            'type':'paid',
            'amount':getDecimal(post_data['amount']),
            'created_at':str(datetime.datetime.utcnow())[:-3],
            'updated_at':str(datetime.datetime.utcnow())[:-3],
            'memo':''
        }
        try:
            updateData['payment_method_details'] =  pay_result.body['payment']['card_details']
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
    print(pay_result.body)
    return jsonify({"Message":"Success"})