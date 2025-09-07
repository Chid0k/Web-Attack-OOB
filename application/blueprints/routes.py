from flask import Blueprint, redirect, render_template, request, session, url_for
from application.util import *
from application.database import connection, db_login, db_register
from application.blueprints.logs import capture_log
from uuid import uuid4
import os

LISTENER_URL = "http://listener.voyager.id.vn/"
LOG_PATH = "/var/log/apache2" #os.getcwd() # listen.log & listen_post.log

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

##### Login & Register Views #####
@web.route('/', methods=['GET'])
def loginView():
    message = escape(request.args.get('Message', ''))
    return render_template('login.html', Message=message)

@web.route('/register', methods=['GET'])
def registerView():
    message = escape(request.args.get('Message', ''))
    return render_template('register.html', Message=message)

@web.route('/forgot', methods=['GET'])
def forgotView():
    message = escape(request.args.get('Message', ''))
    return render_template('forgot.html', Message=message)

@web.route('/home', methods=['GET'])
@isAuthenticated
def homeView(user):
    return render_template('home.html', user=user, u_link=LISTENER_URL + session['user_uuid'])

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
        return redirect(url_for('web.homeView'), code=302)
    else:
        return redirect(url_for('web.loginView', Message=db_login(account, password)[1]), code=302)

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
        return redirect(url_for('web.registerView', Message='Invalid email address'), code=302)
    else:
        email = filterInput(email)
    if db_register(name, email, account, password)[0] == True:
        return redirect(url_for('web.loginView', Message="Registration successful. Please log in."), code=302)
    return redirect(url_for('web.registerView', Message=db_register(name, email, account, password)[1]), code=302)

@api.route('/forgot', methods=['POST'])
def forgot():
    return response('Function under maintenance')

@api.route('/logout', methods=['GET'])
@isAuthenticated
def logout(user):
    session.pop('user', None)
    session.pop('user_uuid', None)
    return redirect(url_for('web.loginView'), code=302)

@api.route('/log', methods=['GET'])
@isAuthenticated
def get_log(user):
    uuid = session['user_uuid']
    # file_path_log = os.path.join(LOG_PATH, 'logs', 'access.log')
    logs = capture_log(LOG_PATH + "/listen.log", uuid)
    return logs


