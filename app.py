from operator import pos
import logging
from flask import Flask, json, jsonify, request, session, send_file
from flask.templating import render_template
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from decimal import *
import config

import json

import datetime

from werkzeug.utils import redirect

import bcrypt
import pymongo

from bson.objectid import ObjectId

# setting up logging
logger = logging.getLogger('PureTalk')

logger.setLevel(logging.DEBUG)

todayFormatted = (datetime.datetime.today()).strftime("%Y-%m-%d")

fh = logging.FileHandler('logs/puretalk-{}.py.log'.format(todayFormatted))
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] - %(name)14s - %(levelname)8s | %(message)s","%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)

logger.addHandler(fh)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = '2abceVR5ENE7FgMxXdMwuzUJKC2g8xgy'

cors = CORS(app, resources={r"/api/v2": {"origins": "*"}, r"/leads/generator": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.mongo_client = pymongo.MongoClient("mongodb+srv://puretalk:9PVQrICWzRBGVaSD@cluster0.vc0rw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# BLUEPRINT
from pureApi import apiBlueprint, convertToJSON
from customerAPI import customerApiBlueprint
from pureApi import unsetCompanyID


from vicidialAPI import viciApiBlueprint
from routes import logBlueprint, campaignsBlueprint, leadsBlueprint, twilioBlueprint, conversationFlow, plivoBlueprint, ttsBlueprint, squareAPI

app.register_blueprint(apiBlueprint)
app.register_blueprint(customerApiBlueprint)
app.register_blueprint(viciApiBlueprint)
app.register_blueprint(logBlueprint.logBlueprint)
app.register_blueprint(campaignsBlueprint.campaignsBlueprint)
app.register_blueprint(leadsBlueprint.leadsBlueprint)
app.register_blueprint(twilioBlueprint.twilioBlueprint)
app.register_blueprint(squareAPI.squareBlueprint)
app.register_blueprint(conversationFlow.conversationBlueprint)
app.register_blueprint(plivoBlueprint.plivoBlueprint)
app.register_blueprint(ttsBlueprint.ttsBlueprint)

version = '1.3.9.7'

def connectToDB():
    mongoDB = app.mongo_client['jamesbon']
    return mongoDB

def validateLogin():
    try:
        if session['user']:
            try:
                if session['version'] == version:
                    session['debug'] = config.debug
                    
                    #client = app.mongo_client
                    mongoDB = app.mongo_client['jamesbon']
                    user_col = mongoDB['users']
                    user = user_col.find_one({'_id':ObjectId(session['user']['user_id'])})
                    #client.close()
                    try:
                        session['user']['tour_complete'] = user['tour_complete']
                    except:
                        session['user']['tour_complete'] = False
                    return True
                else:
                    session.clear()
                    return False
            except:
                session.clear()
                return False
        else:
            return False
    except:
        return False

def validateCompany(companyID):
    try:
        if int(companyID) in session['companies']:
            return True
    except:
        pass
    return False

@app.route('/')
def index():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/index.html', companyName='PureTalk', pageTitle='Dashboard', navPosition='index')
            return render_template('vicidial/index.html', companyName='PureTalk', pageTitle='Dashboard', navPosition='index')
        else:
            return redirect('/super-admin')

    return redirect('/login')

@app.route('/super-admin')
def indexAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            companies = getCompanies("created_at", pymongo.DESCENDING)
            return render_template('index-admin.html', companyName='PureTalk', pageTitle='Dashboard', companyImg='9867959136a2357fbe9eb7d4f93d9e87.png', navPosition='index', companies=companies)

    return redirect('/login')

@app.route('/switch-company')
def switchCompany():
    if validateLogin():
        updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
        unsetCompanyID()
        if session['user']['super_admin'] == 0:
            return redirect('/select-company')
        return redirect('/companies')

    return redirect('/login')

@app.route('/select-company')
def selectCompany():
    if validateLogin():
        if session['user']['super_admin'] == 0:
            if session['user']['company_id'] == None:
                updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                companies = getCompanies()
                return render_template('/company-select.html', companyName='PureTalk', pageTitle='Dashboard', navPosition='index', companies=companies)
            else:
                return redirect('/super-admin')
            
        return redirect('/select-company')

    return redirect('/login')

@app.route('/articles')
def articles():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('articles.html', companyName='PureTalk', pageTitle='Articles', companyImg='9867959136a2357fbe9eb7d4f93d9e87.png', navPosition='articles')
    return redirect('/login')

@app.route('/subscription-plans')
def subscriptionPlans():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('subscription-plans.html', companyName='PureTalk', pageTitle='Subscription Plans', companyImg='9867959136a2357fbe9eb7d4f93d9e87.png', navPosition='subscriptions')
    return redirect('/login')

@app.route('/companies')
def companies():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            mongoDB = app.mongo_client['jamesbon']
            companies = mongoDB['companies']
            unsetCompanyID()
            companies = getCompanies("created_at", pymongo.DESCENDING)
            return render_template('companies.html', companyName='PureTalk', pageTitle='Companies', companyImg='9867959136a2357fbe9eb7d4f93d9e87.png', navPosition='companies', companies=companies)
    return redirect('/login')

@app.route('/ai-agents-admin')
def aiAgentsAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('ai-agents-admin.html', companyName='PureTalk', pageTitle='Companies', companyImg='9867959136a2357fbe9eb7d4f93d9e87.png', navPosition='ai-agents-admin')
    return redirect('/login')

@app.route('/virtual-agents-admin')
def virtualAgentsAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('virtual-agents-admin.html', companyName='PureTalk', pageTitle='Virtual Agents', companyImg='9867959136a2357fbe9eb7d4f93d9e87.png', navPosition='virtual-agents-admin')
    return redirect('/login')

@app.route('/super-admin-edit')
def superAdminEdit():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            users = getUsers(True)
            return render_template('super-admins.html', companyName='PureTalk', pageTitle='Companies', companyImg='9867959136a2357fbe9eb7d4f93d9e87.png', navPosition='super-admin-edit', users=users)
    return redirect('/login')

@app.route('/ai-agents')
def aiAgents():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('vicidial/ai-agents.html', companyName='PureTalk', pageTitle='AI Agents', navPosition='index', navTab='')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/call-manager')
def callManager():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/call-manager.html', companyName='PureTalk', pageTitle='Call Manager', navPosition='call-manager', navTab='campaign-manager')
            return render_template('vicidial/call-manager.html', companyName='PureTalk', pageTitle='Call Manager', navPosition='call-manager', navTab='campaign-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')
        
@app.route('/campaigns')
def campaigns():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/campaigns.html', companyName='PureTalk', pageTitle='Campaigns', navPosition='campaigns', navTab='campaign-manager')
            return render_template('vicidial/campaigns.html', companyName='PureTalk', pageTitle='Campaigns', navPosition='campaigns', navTab='campaign-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')
        
@app.route('/campaigns-breakdown')
def campaignBreakdown():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('twilio/campaign-cost-breakdown.html', companyName='PureTalk', pageTitle='Campaigns Cost Breakdown', navPosition='campaigns', navTab='campaigns-breakdown')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/call-history')
def callHistory():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/callhistory.html', companyName='PureTalk', pageTitle='Call History', navPosition='call-history', navTab='lead-manager', campaign=request.args.get('campaignid'))
            return render_template('vicidial/callhistory.html', companyName='PureTalk', pageTitle='Leads', navPosition='leads', navTab='lead-manager', campaign=request.args.get('campaignid'))
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/leads')
def leads():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/leads.html', companyName='PureTalk', pageTitle='Leads', navPosition='leads', navTab='lead-manager', campaign=request.args.get('campaignid'))
            return render_template('vicidial/leads.html', companyName='PureTalk', pageTitle='Leads', navPosition='leads', navTab='lead-manager', campaign=request.args.get('campaignid'))
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/unknown-intents')
def unkownIntents():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('twilio/unkown-intents.html', companyName='PureTalk', pageTitle='NLU Inbox', navPosition='unkown-intents', navTab='campaign-manager', campaign=request.args.get('campaignid'))
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/dnc')
def dnc():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/dnc.html', companyName='PureTalk', pageTitle='Leads', navPosition='leads', navTab='lead-manager', campaign=request.args.get('campaignid'))
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/lists')
def lists():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('vicidial/lists.html', companyName='PureTalk', pageTitle='Leads', navPosition='lists', navTab='lead-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/leads-list')
def leadsList():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('vicidial/leads-list.html', companyName='PureTalk', pageTitle='Leads', navPosition='leads-list', navTab='lead-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')

@app.route('/agree')
def disclaimerAgree():
    updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
    mongoDB = app.mongo_client['jamesbon']
    agreement_col = mongoDB['agreement_sign']
    insert_query = {
        'user_id':ObjectId(session['user']['user_id']),
        'company_id':ObjectId(session['company']['id']),
        'signed_date':datetime.datetime.utcnow()
    }
    agreement_col.insert_one(insert_query)
    session['lead-agreement'] = True
    return redirect('/import-leads')

@app.route('/import-leads')
def importLeads():
    if validateLogin():
        if session['user']['company_id']:
            try:
                if session['lead-agreement']:
                    session['lead-agreement'] = False
                    updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
                    if session['call_type'] == 'twilio':
                        return render_template('twilio/import-leads.html', companyName='PureTalk', pageTitle='Import Leads', navPosition='import-leads', navTab='lead-manager')
                    return render_template('vicidial/import-leads.html', companyName='PureTalk', pageTitle='Import Leads', navPosition='import-leads', navTab='lead-manager')
            except:
                session['lead-agreement'] = False
                
            if session['call_type'] == 'twilio':
                return render_template('twilio/import-lead-agreement.html', companyName='PureTalk', pageTitle='Import Lead Agreement', navPosition='import-leads', navTab='lead-manager')
            return render_template('vicidial/import-lead-agreement.html', companyName='PureTalk', pageTitle='Import Lead Agreement', navPosition='import-leads', navTab='lead-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/export-leads')
def exportLeads():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/export-leads.html', companyName='PureTalk', pageTitle='Export Leads', navPosition='export-leads', navTab='lead-manager')
            return render_template('vicidial/export-leads.html', companyName='PureTalk', pageTitle='Export Leads', navPosition='export-leads', navTab='lead-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/import-caller-ids')
def importCallerIDs():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/import-caller-ids.html', companyName='PureTalk', pageTitle='Import Caller IDs', navPosition='import-caller-ids', navTab='lead-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/caller-ids')
def callerIDs():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/caller-ids.html', companyName='PureTalk', pageTitle='Caller IDs', navPosition='caller-ids', navTab='lead-manager')
            return render_template('vicidial/caller-ids.html', companyName='PureTalk', pageTitle='Caller IDs', navPosition='caller-ids', navTab='lead-manager')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/follow-up-calls')
def followUpCalls():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('vicidial/follow-up-calls.html', companyName='PureTalk', pageTitle='Follow Up Calls', navPosition='follow-up-calls', navTab='appointments')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/staff-members')
def staffMembers():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            users = getUsers(False)
            return render_template('staff-members.html', companyName='PureTalk', pageTitle='Staff Members', navPosition='staff-members', navTab='user-management', users=users)
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/staff-members-admin')
def staffMembersAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            users = getUsers(False)
            return render_template('staff-members-admin.html', companyName='PureTalk', pageTitle='Staff Members', navPosition='staff-members', navTab='user-management', users=users)

    return redirect('/login')
    
@app.route('/sales-members')
def salesMembers():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('sales-members.html', companyName='PureTalk', pageTitle='Sales Members', navPosition='sales-members', navTab='user-management')
        else:
            return redirect('/super-admin')

    return redirect('/login') 
    
@app.route('/sales-members-admin')
def salesMembersAdmin():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('vicidial/sales-members.html', companyName='PureTalk', pageTitle='Sales Members', navPosition='sales-members', navTab='user-management')
        else:
            return redirect('/super-admin')

    return redirect('/login') 
    
@app.route('/roles-admin')
def rolesAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('roles-admin.html', companyName='PureTalk', pageTitle='Role Setup', navPosition='roles', navTab='user-management')

    return redirect('/login')
    
@app.route('/roles')
def roles():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            return render_template('roles.html', companyName='PureTalk', pageTitle='Role Setup', navPosition='roles', navTab='user-management')

    return redirect('/login')
    
@app.route('/billing')
def billing():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/billing.html', companyName='PureTalk', pageTitle='Billing', navPosition='billing', navTab='settings')
            return render_template('twilio/billing.html', companyName='PureTalk', pageTitle='Billing', navPosition='billing', navTab='settings')
        else:
            return redirect('/super-admin')

    return redirect('/login') 
    
@app.route('/billing-admin')
def billingAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            companies = getCompanies()
            return render_template('twilio/billing-admin.html', companyName='PureTalk', pageTitle='Billing', navPosition='billing', navTab='settings', companies=companies)

    return redirect('/login') 
    
@app.route('/billing-twilio')
def billingTwilioAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            companies = getCompanies()
            return render_template('twilio-billing.html', companyName='PureTalk', pageTitle='Billing', navPosition='billing', navTab='settings', companies=companies)

    return redirect('/login') 
    
@app.route('/profile-twilio')
def profileTwilioAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            companies = getCompanies()
            return render_template('twilio-profile.html', companyName='PureTalk', pageTitle='Billing', navPosition='billing', navTab='settings', companies=companies)

    return redirect('/login') 
    
@app.route('/form-builder')
def formBuilder():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/form-builder.html', companyName='PureTalk', pageTitle='Form Builder', navPosition='form-builder', navTab='settings')
            return render_template('vicidial/form-builder.html', companyName='PureTalk', pageTitle='Form Builder', navPosition='form-builder', navTab='settings')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/field-mappings')
def formMappings():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/field-mappings.html', companyName='PureTalk', pageTitle='Form Mappings', navPosition='field-mappings', navTab='settings')
            return render_template('vicidial/field-mappings.html', companyName='PureTalk', pageTitle='Form Mappings', navPosition='field-mappings', navTab='settings')
        else:
            return redirect('/super-admin')

    return redirect('/login')
    
@app.route('/twilio')
def twilioAdmin():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/twilio-numbers.html', companyName='PureTalk', pageTitle='Form Builder', navPosition='form-builder', navTab='settings')

    return redirect('/login')  
    
@app.route('/settings')
def settings():
    if validateLogin():
        if session['user']['company_id']:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            if session['call_type'] == 'twilio':
                return render_template('twilio/settings.html', companyName='PureTalk', pageTitle='Settings', navPosition='settings', navTab='settings')
            return render_template('vicidial/settings.html', companyName='PureTalk', pageTitle='Settings', navPosition='settings', navTab='settings')
        else:
            return redirect('/super-admin')

    return redirect('/login') 
    
@app.route('/settings-admin')
def settingsAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('settings-admin.html', companyName='PureTalk', pageTitle='Settings', navPosition='settings', navTab='settings')
        else:
            return redirect('/')
    
@app.route('/twilio-summary')
def twilioSummaryAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            companies = getCompanies()
            return render_template('twilio/twilio-billing-breakdown.html', companyName='PureTalk', pageTitle='Settings', navPosition='settings', navTab='settings', companies=companies)
        else:
            return redirect('/')
    
@app.route('/logs')
def logsAdmin():
    if validateLogin():
        if session['user']['super_admin'] == 1 and session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('logs.html', companyName='PureTalk', pageTitle='Logs', navPosition='log-admin', navTab='log-admin')
        else:
            return redirect('/')
    
@app.route('/sandbox')
def sandboxAdmin():
    return render_template('twilio/sandbox.html', companyName='PureTalk', pageTitle='Settings', navPosition='settings', navTab='settings')
    
@app.route('/chat-stories')
def chatStories():
    if validateLogin():
        if session['user']['super_admin'] == 1:
            updateUserLog(request.path, str(request.environ.get('HTTP_X_FORWARDED_FOR')).split(','))
            unsetCompanyID()
            return render_template('chat-bot/stories.html', companyName='PureTalk', pageTitle='Settings', navPosition='settings', navTab='settings')
        else:
            return redirect('/')

    return redirect('/login') 
    
@app.route('/twilio_calculator')
def twilioCalculatorAdmin():
    return render_template('twiliocalculator.html', companyName='PureTalk', pageTitle='Form Builder', navPosition='form-builder', navTab='settings')

@app.route('/agent-login', methods=['GET', 'POST'])
def agentLogin():
    if request.method == 'GET':
        if request.args.get('campaignid'):
            session['agent-campaign'] = request.args.get('campaignid')
            session['agent-campaign-name'] = request.args.get('campaignname')
            return redirect('/agent-dashboard')
        try:
            if session['agent-campaign']:
                return redirect('/agent-dashboard')
            elif request.args.get('campaignid'):
                session['agent-campaign'] = request.args.get('campaignid')
                return redirect('/agent-dashboard')
        except:
            pass
        return render_template('twilio/agent-login.html')
    elif request.method == 'POST':
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaigns_col = mongoDB['campaigns']
        search_query = {
            "_id":ObjectId(request.form.get('campaign'))
        }
        campaign = campaigns_col.find_one(search_query)
        if campaign:
            session['agent-campaign-name'] = campaign['name']
            session['agent-campaign'] = request.form.get('campaign')
            return redirect('/agent-dashboard')
        else:
            return render_template('twilio/agent-login.html')

@app.route('/agent-logout', methods=['GET'])
def agentLogout():
    if request.method == 'GET':
        try:
            session.pop('agent-campaign-name')
            session.pop('agent-campaign')
        except:
            pass
        return render_template('twilio/agent-login.html')
        
@app.route('/agent-dashboard')
def agentDashboard():
    try:
        if session['agent-campaign']:
            return render_template('twilio/agent-dashboard.html')
    except:
        pass
    return redirect('/agent-login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if validateLogin():
            if session['user']['super_admin'] == 1:
                if session['user']['company_id']:
                    return redirect('/')
                else:
                    return redirect('/super-admin')
            else:
                if session['user']['company_id']:
                    return redirect('/')
                return redirect('/select-company')
        try:
            message = session['message']
            session.pop('message')
        except:
            message = None
        session['version'] = version
        if config.debug == True:
            return render_template('vicidial/login.html', companyName='PureTalk', pageTitle='Login', navPosition='index', message=message)
        else:
            return render_template('vicidial/login.html', companyName='PureTalk', pageTitle='Login', navPosition='index', message=message)
    elif request.method == 'POST':
        session.clear()
        username = request.form['username']
        password = bytes(request.form['password'], 'utf-8')
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        users = mongoDB['users']
        filterBy = {
            "email":username
        }
        logger.debug(str(request.headers))
        print(request.headers)
        referrer = request.referrer
        if referrer == 'https://d60bcc9a-c232-411f-93fb-bdbe51d252cf.htmlcomponentservice.com/':
            referrer = 'https://www.realtalk-ai.com/'
        session['referrer'] = referrer
        for user in users.find(filterBy):
            if user['status'] == 'enabled':
                if bcrypt.checkpw(password,bytes(user['password'], 'utf-8')):
                    session['user'] = {
                        'company_id':str(user['company_id']),
                        'first_name':user['first_name'],
                        'last_name':user['last_name'],
                        'email':user['email'],
                        'image':user['image'],
                        'super_admin':user['super_admin'],
                        'user_id':str(user['_id'])
                    }
                    try:
                        session['user']['tour_complete'] = user['tour_complete']
                    except:
                        session['user']['tour_complete'] = False
                    roleUsers = mongoDB['role_user_new']
                    roleUserFilterBy = {
                        "user_id":user['_id']
                    }
                    companyList = []
                    permission_sets = {}
                    if str(user['_id']) == '613b8a785a2cd24ac1a33bc0':
                        companies = mongoDB['companies']
                        for company in companies.find():
                            companyList.append(str(company['_id']))
                    else:
                        for roleUser in roleUsers.find(roleUserFilterBy):
                            roleFilterBy = {
                                "_id":roleUser['role_id']
                            }
                            roles_col = mongoDB['roles']
                            role = roles_col.find_one(roleFilterBy)
                            if role:
                                companyList.append(str(role['company_id']))
                                permission_sets[str(role['company_id'])] = {}
                                for permission in role['permissions']:
                                    try:
                                        perm_disp_name = str(permission['display_name'])
                                    except:
                                        perm_disp_name = ''
                                    permission_sets[str(role['company_id'])][str(permission['_id'])] = {
                                        "name":str(permission['name']),
                                        "display_name":perm_disp_name,
                                        "id":str(permission['_id'])
                                    }
                            
                    session['permission_sets'] = permission_sets
                    session['companies'] = companyList
                    session['user']['company_id'] = None
                    
                    session['version'] = version
                    session['company'] = {}
                    if user['company_id']:
                        company_col = mongoDB['companies']
                        companyFilterBy = {
                            '_id':user['company_id']
                        }
                        company = company_col.find_one(companyFilterBy)
                        if company:
                            session['company'] = {
                                'logo': company['logo'], 
                                'package_type': company['package_type'], 
                                'name': company['name'], 
                                'email': company['email'], 
                                'phone': company['phone'], 
                                'website': company['website'], 
                                'address': company['address'], 
                                'app_layout': company['app_layout'], 
                                'rtl': company['rtl'], 
                                'status': company['status']
                            }
                    if session['user']['company_id'] == None and session['user']['super_admin'] == 0:
                        return redirect('/select-company')
                    return redirect('/super-admin')
        return redirect(session['referrer'])

@app.route('/api-docs', methods=['GET'])
def apiDocs():
    return render_template('vicidial/api-docs.html', companyName='PureTalk', pageTitle='Login', navPosition='index')

@app.route('/etc/ruth', methods=['GET'])
def downloadRuth():
    return send_file("./static/ruth_nlu.zip", as_attachment=True)

@app.route('/convo/projects', methods=['GET'])
def convoProjects():
    mongoDB = app.mongo_client['conversation-flow']
    flows_col = mongoDB['flows']
    flows = []
    for flow in flows_col.find():
        flowData = convertToJSON(flow)
        flows.append(flowData)
    return render_template('projects.html', companyName='PureTalk', pageTitle='Login', navPosition='index', flows=flows)

@app.route('/convo/builder', methods=['GET'])
def convoBuilder():
    return render_template('line.html', companyName='PureTalk', pageTitle='Login', navPosition='index')

@app.route('/user-sign-up', methods=['GET', 'POST'])
def userSignUp():
    if request.method == 'GET':
        if request.args.get('token'):
            session['signup-token'] = request.args.get('token')
        try:
            if session['signup-token']:
                mongoDB = app.mongo_client['jamesbon']
                signup_tokens_col = mongoDB['signup_tokens']
                signup_token = signup_tokens_col.find_one({'_id':ObjectId(session['signup-token'])})
                users_col = mongoDB['users']
                users = users_col.find_one({'_id':signup_token['user_id']})
                token = session['signup-token']
                session.clear()
                session['signup-token'] = token
                return render_template('user-signup.html', email=users['email'])
        except:
            pass
    elif request.method == 'POST':
        mongoDB = app.mongo_client['jamesbon']
        signup_tokens_col = mongoDB['signup_tokens']
        signup_token = signup_tokens_col.find_one({'_id':ObjectId(session['signup-token'])})
        filter_by = {
            '_id':signup_token['user_id']
        }

        ## SALT PASSWORD
        password = bytes(request.form.get('password'), 'utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        password = str(hashed)[2:]
        password = str(password)[:-1]

        update_data = {
            "$set":{
                "password":password,
                "status":"enabled"
            }
        }
        users_col = mongoDB['users']
        users_col.update_one(filter_by, update_data)
        return redirect('/login')
    return 'unauthorized'

@app.route('/logout')
def logout():
    if config.debug == True:
        try:
            redirect_site = session['referrer']
        except:
            redirect_site = '/login'
        session.clear()
        return redirect(redirect_site)
    else:
        try:
            redirect_site = session['referrer']
            if redirect_site == '' or redirect_site == None:
                redirect_site = 'https://puretalk.ai/login'

        except:
            redirect_site = 'https://puretalk.ai/login'
        session.clear()
        return redirect(redirect_site)

def formatDate(myDate):
    return myDate.strftime("%Y/%m/%d")
    
def formatNiceDate(myDate):
    return myDate.strftime("%m/%d/%Y")

def formatDateStd(myDate):
    return myDate.strftime("%Y-%m-%d")

def getDecimal(x):
    try:
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return float(x)
    except:
        x = 0
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return float(x)

def getInt(x):
    try:
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)
    except:
        x = 0
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)

def formatStringToJSON(x):
    try:
        leadData = str(x).replace("'\"", "'\\\"")
        leadData = str(leadData).replace("\"'", "\\\"'")
        leadData = str(leadData).replace("'", '"')
        return json.loads(leadData)
    except:
        leadData = str(x).replace("'\"", "'\\\"")
        leadData = str(leadData).replace("\"'", "\\\"'")
        leadData = str(leadData).replace("'", '"')
        print(leadData)

def getCampaigns():
    #client = app.mongo_client
    mongoDB = app.mongo_client['jamesbon']
    campaigns_col = mongoDB['campaigns']
    filterBy = {}
    if session['user']['company_id']:
        filterBy['company_id'] = ObjectId(session['user']['company_id'])
    returnPost = []
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
        returnPost.append(campaignData)
    #client.close()
    return returnPost

def getCompanies(sort_col="name", sort_style=pymongo.ASCENDING):
    #client = app.mongo_client
    mongoDB = app.mongo_client['jamesbon']
    companies = mongoDB['companies']
    company_list = []
    filterBy = {}
    for company in session['companies']:
        company_list.append(ObjectId(company))
    filterBy = {
        "_id":{
            "$in" : company_list
        }
    }
    returnPost = []
    for company in companies.find(filterBy).sort([(sort_col, sort_style)]):
        logoName = '/static/img/brand/default.png'
        companyData = convertToJSON(company)
        if company['logo']:
            logoName = '/static/img/brand/'+str(company['logo'])
        companyData['logo'] = logoName

        companyData['total_users'] = 0
        returnPost.append(companyData)
    #client.close()
    return returnPost

def getUsers(superadmin):
    #client = app.mongo_client
    mongoDB = app.mongo_client['jamesbon']
    users = mongoDB['users']
    company_list = []
    filterBy = {}
    roleFilterBy = {}
    roleUserFilter = {}
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
    filterBy['super_admin'] = superadmin
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
                #roles.append(convertToJSON(role))
        if userData['last_name'] == None:
            userData['last_name'] = ''
        returnPost['users'].append(userData)
    #client.close()
    return returnPost['users']

def updateUserLog(location, remote_addr):
    try:
        mongoDB = app.mongo_client['logs']
        users_log_col = mongoDB['users']
        try:
            company_id = ObjectId(session['company']['id'])
        except:
            company_id = None
        insert_query = {
            'user_id':ObjectId(session['user']['user_id']),
            'company_id':company_id,
            'location':location,
            'ip': remote_addr[0],
            'created_at':str(datetime.datetime.utcnow())[:-3]
        }
        users_log_col.insert(insert_query)
    except:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=config.debug)
