
# example of application/utils/payload.py
import json

# payload = {'path': "test_path", 
#            'headers': ["Header1: Value2", "Header2: Value2"], 
#            'data': "sample data", 
#            'content_type': "application/json", 
#            'username': "testuser"
#            }


def generate_payload(_payload):
    with open(f"payload/{_payload['userid']}.txt", "w+") as f:
        f.write(json.dumps(_payload, indent=4))

def load_payload(userid):
    try:
        with open(f"payload/{userid}.txt", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return False
    
def detele_payload(userid):
    try:
        import os
        os.remove(f"payload/{userid}.txt")
    except FileNotFoundError:
        return None