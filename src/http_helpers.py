import requests
import json


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


###################
# Helper functions
###################
def register_user(url, user):
    # Registers a new user
    r = requests.post(f"{url}/auth/register", json = user)
    return r.json()

def login_user(url, user):
    # Registers a new user
    requests.post(f"{url}/auth/login", json = {
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
    payload["name"] = new_channel["name"]
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
