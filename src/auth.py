from error import InputError, AccessError
from global_dic import data
from utils import generate_token
import uuid
import re
import hashlib
from appsecret import JWT_SECRET


#Validate Email
def validate_Email(email):
    emailPattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    #Email length less than 255
    if len(email) > 254:
        raise InputError(InputError)
    #Email length must be more than 0
    if len(email) == 0:
        raise InputError(InputError)
    if re.search(emailPattern, email) == None:
        raise InputError(InputError)


def auth_login(email, password):
    #Boolean if the email is found
    find = False
    #Function to validate email
    validate_Email(email)
    if len(password) == 0:
        raise InputError(InputError)
    #Check if email exist
    for i in range(len(data["users"])):
        if (data["users"][i]["email"] == email):
            find = True
            u_id = data['users'][i]['u_id']
            #Check if a token exist for that user
            if ('u_token' in data['users'][i]):
                u_token = data['users'][i]['u_token']
            else:
                user_token = generate_token(u_id)
            #Check if hashed password match
            if (data["users"][i]["password"] != hashlib.sha256(
                    str(password).encode('utf-8')).hexdigest()):
                raise InputError(InputError)
            else:
                data["users"][i]["state"] = "active"
    #Input error if user not found
    if find == False:
        raise InputError(InputError)

    return {
        'u_id': u_id,
        'u_token': u_token,
    }


def auth_logout(token):
    find = False
    for i in range(len(data["users"])):
        #Find token
        if (data["users"][i]["u_token"] == token):
            if (data["users"][i]['state'] != "active"):
                raise AccessError(AccessError)
            data["users"][i]['state'] = "inactive"
            #Remove token
            del data["users"][i]["u_token"]
            find = True
    if find == False:
        raise AccessError(AccessError)
    return {
        'is_success': True,
    }


def auth_register(email, password, name_first, name_last):
    validate_Email(email)
    if len(password) < 6:
        raise InputError(InputError)
    if len(password) > 18:
        raise InputError(InputError)
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(InputError)
    if (re.search("^[a-zA-Z]+[a-zA-Z]$", name_first) == None):
        raise InputError(InputError)
    if (re.search("^[a-zA-Z]+[a-zA-Z]$", name_last) == None):
        raise InputError(InputError)
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(InputError)
    for i in range(len(data["users"])):
        if (data["users"][i]["email"] == email):
            raise InputError(InputError)

    user_id = uuid.uuid4().hex
    user_token = generate_token(user_id)
    password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    data["users"].append({
        "u_id": user_id,
        "u_token": user_token,
        "email": email,
        "first_name": name_first,
        "last_name": name_last,
        "status": "inactive",
        "password": password,
        'handle': name_first.lower() + name_last.lower()
    })
    return {
        'u_id': user_id,
        'u_token': user_token,
    }
