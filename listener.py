from flask import Flask, request
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["2000 per day", "500 per hour"]  # giới hạn mặc định
)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("5 per second") 
def listener():
    return "Listener is active"

@app.route('/<id>', methods=['GET', 'POST'])
@limiter.limit("5 per second") 
def listener_id(id):
    return f"Your request ID be captured: {id}"

@app.route('/favicon.ico', methods=['GET', 'POST'])
@limiter.limit("5 per second") 
def favicon():
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)