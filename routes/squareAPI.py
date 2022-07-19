from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from app import session, app, logger
import pymongo
from bson.objectid import ObjectId

from univFuncs import *
import config
import uuid

#from square.client import Client
from square.client import Client as SquareClient


squareBlueprint = Blueprint('squareAPI', __name__)

SQUARE_ACCESS_TOKEN = 'EAAAEBn_K2QBKzBQqjB3-XL2haWsArbenp2FsdlAVEgVCwK3WAhWKI9eh1E_wnwg'
app.square_client = SquareClient(
    access_token=SQUARE_ACCESS_TOKEN,
    environment='sandbox',
)

@squareBlueprint.route('/api/v1/square/coff', methods=['GET'])
def squareGetCOFF():
    if validateLogin():
        if request.args.get('companyid'):
            companyID = request.args.get('companyid')
            print(companyID)
            if validateCompany(companyID):
                mongoDB = app.mongo_client['jamesbon']
                company_saved_cards_col = mongoDB['company_saved_cards']
                filter_by = {
                    "company_id":ObjectId(companyID)
                }
                coffs = company_saved_cards_col.find(filter_by)
                returnPost = []
                for coff in coffs:
                    returnPost.append(convertToJSON(coff))
                return jsonify(returnPost)
    return jsonify({'Message':'Failure'})

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
    try:
        customer_id = company['square_cust_id']
    except:
        customer_id = create_customer(search_query)

    pay_result = None
    
    if(post_data['use_coff']):
        print('Using COFF')
        print(post_data['sourceId'])
        pay_result = create_payment(post_data, post_data['sourceId'], customer_id)
    else:
        if post_data['save_card']:
            coff = create_card(post_data, customer_id)
            print(coff)
            pay_result = create_payment(post_data, coff, customer_id)
        else:
            pay_result = create_payment(post_data, post_data['sourceId'], customer_id)
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

def create_customer(search_query):
    mongoDB = app.mongo_client['jamesbon']
    companies_col = mongoDB['companies']
    cust_id = str(uuid.uuid4())
    customer_result = app.square_client.customers.create_customer(
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
    return customer_id
    
def create_card(post_data, customer_id):
    card_id = str(uuid.uuid4())
    result = app.square_client.cards.create_card(
        body = {
            "idempotency_key": card_id,
            "source_id": post_data['sourceId'],
            "card": {
                "cardholder_name": "Amelia Earhart",
                "customer_id": customer_id,
                "reference_id": "user-id-1"
            }
        }
    )
    if result.is_success():
        mongoDB = app.mongo_client['jamesbon']
        company_saved_cards_col = mongoDB['company_saved_cards']

        card_id = result.body['card']['id']
        last_4 = result.body['card']['last_4']
        card_brand = result.body['card']['card_brand']
        card_type = result.body['card']['card_type']
        insert_query = {
            'company_id':ObjectId(post_data['company_id']),
            'square_card_id':card_id,
            'last_4':last_4,
            'card_brand':card_brand,
            'card_type':card_type
        }
        company_saved_cards_col.insert_one(insert_query)
        return result.body['card']['id']
    print(result.errors)

def create_payment(post_data, source_id, customer_id):
    pay_id = str(uuid.uuid4())
    return app.square_client.payments.create_payment(
        body = {
            "source_id": source_id,
            "idempotency_key": pay_id,
            "amount_money": {
                "amount": float(post_data['amount'])*100,
                "currency": "USD"
            },
            "customer_id": customer_id
        }
    )