from flask import Flask, request
from flask import Flask, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
from application.utils.payload import load_payload

import json

app = Flask(__name__)
CORS(app)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["2000 per day", "500 per hour"]  # giới hạn mặc định
)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("5 per second")
@cross_origin()
def listener():
    return "Listener is active"

@app.route('/<id>', defaults={'subpath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE'])
@app.route('/<id>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE'])
@cross_origin()
@limiter.limit("5 per second")
def listener_id(id, subpath):
    payload = load_payload(id)
    if not payload:
        return f"Payload with id {id} not found", 200
    if '/' + subpath == payload['path']:
        res = Response(
            response=payload['data'],
            status=200,
            mimetype=payload['content_type']
        )
        res.headers["X-Server"] = "VoyagerAPI"
        res.headers["X-Powered-By"] = payload['username']
        res.headers["X-Path"] = payload['path']
        return res
    else:
        return f"Path {subpath} not found for id {id}", 200
    



@app.route('/favicon.ico', methods=['GET', 'POST'])
@limiter.limit("5 per second")
@cross_origin()
def favicon():
    return ("", 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
