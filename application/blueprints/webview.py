from flask import Blueprint, redirect, render_template, request, session, url_for
from application.utils.auth import *
from application.utils.logs import capture_log
from application.database import connection, db_login, db_register, db_profile

from uuid import uuid4
import os

LISTENER_URL = "https://listener.voyager.id.vn/"
LOG_PATH = "/var/log/apache2" #os.getcwd() # listen.log & listen_post.log

webview = Blueprint('webview', __name__)

##### Authentication #####
@webview.route('/', methods=['GET'])
def loginView():
    if session.get('user'):
        return redirect(url_for('webview.homeView'), code=302)
    message = escape(request.args.get('Message', ''))
    return render_template('login.html', Message=message)

@webview.route('/register', methods=['GET'])
def registerView():
    message = escape(request.args.get('Message', ''))
    return render_template('register.html', Message=message)

@webview.route('/forgot', methods=['GET'])
def forgotView():
    message = escape(request.args.get('Message', ''))
    return render_template('forgot.html', Message=message)

##### User Views #####
@webview.route('/profile', methods=['GET'])
@isAuthenticated
def profileView(user):
    Message = escape(request.args.get('Message', ''))
    profile = db_profile(user) 
    return render_template('profile.html', userdetail=profile, Message=Message)

##### Log view #####
@webview.route('/home', methods=['GET'])
@isAuthenticated
def homeView(user):
    return render_template('home.html', user=user, u_link=LISTENER_URL + session['user_uuid'])

##### Payload view #####
@webview.route('/payload', methods=['GET'])
@isAuthenticated
def payloadView(user):
    return render_template('payload.html', user=user, u_link=LISTENER_URL + session['user_uuid'], data_view=session['payload'])





