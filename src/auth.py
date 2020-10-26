'''
AUTH
'''
import uuid
from error import InputError
from global_dic import data
from utils import generate_token, check_token, remove_token
from auth_helper import validate_email, validate_password, hash_password, validate_name, check_email, logout_state


def auth_login(email, password):
    '''
    Function to validate email
    '''
    validate_email(email)
    validate_password(password)
    #Input error if user not found
    if check_email(email) == False:
        raise InputError(InputError)

    for i in range(len(data["users"])):
        if data["users"][i]["email"] == email:
            u_id = data['users'][i]['u_id']
            #Check if a token exist for that user
            if ('token' in data['users'][i]):
                token = data['users'][i]['token']
            else:
                token = generate_token(u_id)
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
    '''
    Function to logout
    '''
    check_token(token)
    remove_token(token)
    logout_state(token)
    return {
        'is_success': True,
    }


def auth_register(email, password, name_first, name_last):
    '''
    Function to register user
    '''
    validate_email(email)
    validate_password(password)
    validate_name(name_first)
    validate_name(name_last)
    if check_email(email) == True:
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
        "state": "inactive",
        "password": password,
        'handle': name_first.lower() + name_last.lower()
    })
    return {
        'u_id': user_id,
        'token': user_token,
    }
