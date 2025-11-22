from flask import Flask
from application.blueprints.webview import webview
from application.blueprints.api import api
from application.utils.auth import response
import random
from datetime import timedelta


app = Flask(__name__)
app.secret_key = str(random.getrandbits(128))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


app.register_blueprint(webview, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')

@app.errorhandler(404)
def not_found(error):
    return response('404 Not Found'), 404

@app.errorhandler(403)
def forbidden(error):
    return response('403 Forbidden'), 403

@app.errorhandler(400)
def bad_request(error):
    return response('400 Bad Request'), 400

@app.errorhandler(Exception)
def handle_error(error):
    message = error.description if hasattr(error, 'description') else [str(x) for x in error.args]
    response = {
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return response, error.code if hasattr(error, 'code') else 500

