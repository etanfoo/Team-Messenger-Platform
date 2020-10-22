from datetime import datetime
import jwt
from appsecret import JWT_SECRET
from global_dic import data


def generate_token(user_id):
    '''
    Returns a JWT token based on the users id and a secret message.
    '''
    token = jwt.encode({
        'user_id': user_id,
    }, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    return token


def decode_token(token):
    '''
    decode_token
    '''
    decoded = jwt.decode(token, JWT_SECRET, algorithms='HS256')


def check_token(token):
    '''
    Check if token exist
    '''
    for i in range(len(data["users"])):
        #Find token
        if (data["users"][i]["token"] == token):
            return True
    return False


def remove_token(token):
    for i in range(len(data["users"])):
        #Find token
        if (data["users"][i]["token"] == token):
            del data["users"][i]["token"]
            return True
    return False