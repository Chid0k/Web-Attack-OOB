from flask import jsonify, session, redirect, url_for
from functools import wraps
from markupsafe import escape
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$')

def emailIsValid(email: str) -> bool:
    return EMAIL_REGEX.match(email) is not None

def filterInput(input_str):
    return escape(input_str)

def response(message):
    return jsonify({"message": message})

def isAuthenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')
        if not user:
            return redirect(url_for('webview.loginView'))  
        return f(user=user, *args, **kwargs)
    return decorated_function
