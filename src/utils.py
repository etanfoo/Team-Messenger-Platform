from datetime import datetime
import jwt
from appsecret import JWT_SECRET
from error import AccessError
from global_dic import data
import requests

INVALID_TOKEN = -1000

def get_current_timestamp(delay=0):
    '''
    Return current time + delay as a unix timestamp
    '''
    current_time = datetime.now()
    return int(current_time.timestamp() + delay)


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
    Checks if a jwt token corresponds to a currently logged in user.
    If the user's account has been deleted, invalidates that users token.
    :param token: jwt token
    :type token: str
    :raises AccessError: If the token does not correspond to a logged in user
    :raises AccessError: If the token corresponds to a deleted user
    :return: User id corresponding to the the valid token
    :rtype: int
    '''

    for user in data["users"]:
        if user["token"] == token:
            return True
    #Token does not exist
    raise AccessError("Token does not exist")

        

def check_user_in_channel(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return True
    return False


def remove_token(token):
    global data
    for i in range(len(data["users"])):
        #Find token
        if (data["users"][i]["token"] == token):
            data["users"][i]["token"] = INVALID_TOKEN
            return True
    #Token does not exist
    raise AccessError("Token does not exist")


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

def prepare_user(url, user):
    new_user = register_user(url, user)
    login_user(url, user)
    return new_user

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


def send_message(url, token, channel_id, message):
    message_detail = {
        "token": token, 
        "channel_id": channel_id, 
        "message": message
    }
    return requests.post(f"{url}/message/send", json = message_detail)

def send_message_id(url, token, channel_id, message):
    message_detail = {
        "token": token, 
        "channel_id": channel_id, 
        "message": message
    }
    payload = requests.post(f"{url}/message/send", json = message_detail)
    return payload.json()


def remove_message(url, token, message_id):
    message = {
        "token": token, 
        "message_id": message_id
    }
    return requests.delete(f"{url}/message/remove", json = message)


def edit_message(url, token, message_id, message):
    message = {
        "token": token, 
        "message_id": message_id,
        "message": message
    }
    return requests.put(f"{url}/message/edit", json = message)

def message_sendlater(url, token, channel_id, message, time_sent):
    message = {
        "token": token,
        "channel_id": channel_id,
        "message": message,
        "time_sent": time_sent
    }
    return requests.post(f"{url}/message/sendlater", json = message)

def message_react(url, token, message_id, react_id):
    message = {
        "token": token, 
        "message_id": message_id,
        "react_id": react_id
    }
    return requests.post(f"{url}/message/react", json = message)

def message_unreact(url, token, message_id, react_id):
    message = {
        "token": token, 
        "message_id": message_id,
        "react_id": react_id
    }
    return requests.post(f"{url}/message/unreact", json = message)

def pin_message(url, token, message_id):
    message = {
        "token": token, 
        "message_id": message_id
    }
    return requests.post(f"{url}/message/pin", json = message)

def unpin_message(url, token, message_id):
    message = {
        "token": token, 
        "message_id": message_id
    }
    return requests.post(f"{url}/message/unpin", json = message)

def channel_message(url, token, channel_id, start):
    message = {
        "token": token, 
        "channel_id": channel_id, 
        "start": start
    }
    payload = requests.get(f"{url}/channel/messages", params = message)
    return payload.json()

###################
# Global variables
###################
authorised_user = {
    "email": "validEmail@gmail.com",
    "password": "valid_password",
    "name_first": "Phil",
    "name_last": "Knight",
}


second_user = {
    "email": "validEmail2@gmail.com",
    "password": "valid_password2",
    "name_first": "Donald",
    "name_last": "Trump",
}

unauthorised_user = {
    "email": "unauthorised@gmail.com",
    "password": "ILoveSleep",
    "name_first": "Sleepy",
    "name_last": "Joe",
}