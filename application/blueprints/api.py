from flask import Blueprint, redirect, render_template, request, session, url_for, Response
from application.utils.auth import *
from application.utils.logs import capture_log
from application.utils.payload import *
from application.database import *

from uuid import uuid4
from hashlib import sha256 as sha
import os

LISTENER_URL = "https://listener.voyager.id.vn/"
LOG_PATH = "/var/log/apache2"
api = Blueprint('api', __name__)

##### API Endpoints #####
@api.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    account = filterInput(data.get('account', ''))
    password = filterInput(data.get('password', ''))
    if db_login(account, password)[0] == True:
        session['user'] = account
        session['user_uuid'] = str(uuid4())
        session['payload'] = {'path': '', 'headers': [f'Created by: {account}', 'From: attack.voyager.id.vn'], 'data': '', 'content_type': 'application/x-www-form-urlencoded'}
        return redirect(url_for('webview.homeView'), code=302)
    else:
        return redirect(url_for('webview.loginView', Message=db_login(account, password)[1]), code=302)

@api.route('/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    name = filterInput(data.get('name', ''))
    account = filterInput(data.get('account', ''))
    password = filterInput(data.get('password', ''))
    email = data.get('email', '')
    if not emailIsValid(email):
        return redirect(url_for('webview.registerView', Message='Invalid email address'), code=302)
    else:
        email = filterInput(email)
    if db_register(name, email, account, password)[0] == True:
        return redirect(url_for('webview.loginView', Message="Registration successful. Please log in."), code=302)
    return redirect(url_for('webview.registerView', Message=db_register(name, email, account, password)[1]), code=302)

@api.route('/forgot', methods=['POST'])
def forgot():
    return response('Function under maintenance')

@api.route('/logout', methods=['GET'])
@isAuthenticated
def logout(user):
    detele_payload(session['user_uuid'])
    session.pop('user', None)
    session.pop('user_uuid', None)
    return redirect(url_for('webview.loginView'), code=302)

@api.route('/log', methods=['GET'])
@isAuthenticated
def get_log(user):
    uuid = session['user_uuid']
    # file_path_log = os.path.join(LOG_PATH, 'logs', 'access.log')
    logs = capture_log(LOG_PATH + "/listen.log", uuid)
    return logs

@api.route('/update_profile', methods=['POST'])
@isAuthenticated
def update_profile(user):
    name = filterInput(request.form.get('name', ''))
    email = filterInput(request.form.get('email', ''))
    if not emailIsValid(email):
        return redirect(url_for('webview.profileView', Message='Invalid email address'), code=302)
    success, message = db_change_profile(user, name=name, email=email)
    return redirect(url_for('webview.profileView', Message=message), code=302)

@api.route('/change_password', methods=['POST'])
@isAuthenticated
def change_password(user):
    old_password = filterInput(request.form.get('current_password', ''))
    new_password = filterInput(request.form.get('new_password', ''))
    confirm_new_password = filterInput(request.form.get('confirm_new_password', ''))
    if new_password != confirm_new_password:
        return redirect(url_for('webview.profileView', Message="New passwords do not match."), code=302)
    success, message = db_change_password(user, old_password, new_password)
    return redirect(url_for('webview.profileView', Message=message), code=302)

@api.route('/payload', methods=['POST'])
@isAuthenticated
def payload(user):
    path = request.form.get('path', '')
    headers = request.form.get('headers', f'Created by: {user}\nFrom: attack.voyager.id.vn').splitlines()
    data = request.form.get('data', '')
    content_type = request.form.get('content_type', 'application/x-www-form-urlencoded')

    payload = {
        'path': path,
        'headers': headers,
        'data': data,
        'content_type': content_type,
        'username': user,
        'userid': session['user_uuid']
    }

    session['payload'] = payload
    generate_payload(payload)
    return redirect(url_for('webview.payloadView'), code=302)

    
    
    
    