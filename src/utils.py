from datetime import datetime
import jwt
from appsecret import JWT_SECRET
from global_dic import data
import requests


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
    return jwt.decode(token, JWT_SECRET, algorithms='HS256')['user_id']


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

###################
# Helper functions
###################
def register_user(url, user):
    # Registers a new user
    r = requests.post(f"{url}/auth/register", json = user)
    return r.json()

def register_user_auth(url, user):
    # Registers a new user
    return requests.post(f"{url}/auth/register", json = user)
    

def login_user(url, user):
    # Registers a new user
    return requests.post(f"{url}/auth/login", json = {
        "email": user['email'], 
        "password": user['password']
    })

def create_channel(url, token, name, is_public):
    # Creates a new channel
    new_channel = {
        "token": token,
        "name": name,
        "is_public": is_public,
    }
    r = requests.post(f"{url}/channels/create", json = new_channel)
    payload = r.json()
    payload["name"] = name
    return payload

def invite_channel(url, token, channel_id, u_id):
    # Invites a user to a channel
    invite = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id,
    }
    r = requests.post(f"{url}/channel/invite", json = invite)
    return r.json()

def user_details(email, password):
    user_detail = {
        "email": email,
        "password": password
    }
    return user_detail

if __name__ == "__main__":
    print(decode_token(generate_token("gilbert")))