from error import InputError, AccessError
from global_dic import data
from utils import generate_token
import uuid
import re
from hashlib import sha256
from appsecret import JWT_SECRET
from auth_helper import validate_email, validate_password, hash_password, validate_name, check_email


def auth_login(email, password):
    #Boolean if the email is found
    #Function to validate email
    validate_email(email)
    validate_password(password)
    #Input error if user not found
    if (check_email == False):
        raise InputError(InputError)
    #Check if email exist
    for i in range(len(data["users"])):
        if (data["users"][i]["email"] == email):
            u_id = data['users'][i]['u_id']
            #Check if a token exist for that user
            if ('token' in data['users'][i]):
                token = data['users'][i]['token']
            else:
                user_token = generate_token(u_id)
            #Check if hashed password match
            if (data["users"][i]["password"] != hash_password(password)):
                raise InputError(InputError)
            else:
                data["users"][i]["state"] = "active"

    return {
        'u_id': u_id,
        'token': token,
    }


def auth_logout(token):
    find = False
    for i in range(len(data["users"])):
        #Find token
        if (data["users"][i]["token"] == token):
            if (data["users"][i]['state'] != "active"):
                raise AccessError(AccessError)
            data["users"][i]['state'] = "inactive"
            #Remove token
            del data["users"][i]["token"]
            find = True
    if find == False:
        raise AccessError(AccessError)
    return {
        'is_success': True,
    }


def auth_register(email, password, name_first, name_last):
    validate_email(email)
    validate_password(password)
    validate_name(name_first)
    validate_name(name_last)
    if (check_email == True):
        raise InputError(InputError)
    user_id = uuid.uuid4().hex
    user_token = generate_token(user_id)
    password = hash_password(password)
    data["users"].append({
        "u_id": user_id,
        "token": user_token,
        "email": email,
        "first_name": name_first,
        "last_name": name_last,
        "status": "inactive",
        "password": password,
        'handle': name_first.lower() + name_last.lower()
    })
    return {
        'u_id': user_id,
        'token': user_token,
    }
