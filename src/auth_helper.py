'''
AUTH_HELPER FUNCTION
'''
import re
import hashlib
from error import InputError, AccessError
from global_dic import data
from utils import decode_token


#Validate Email
def validate_email(email):
    '''
    Make sure email is valid
    '''
    e_pattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    #Email length less than 255
    if len(email) > 254:
        raise InputError("Input 1")
    #Email length must be more than 0
    if len(email) == 0:
        raise InputError("Input 2")
    if re.search(e_pattern, email) is None:
        raise InputError("Input 3")


def validate_password(password):
    '''
    Make sure password comply
    '''
    if len(password) < 6:
        raise InputError("Input 4")
    if len(password) > 18:
        raise InputError("Input 5")


def hash_password(password):
    '''
    Encrypt password with SHA256
    '''
    return hashlib.sha256(str(password).encode('utf-8')).hexdigest()


def validate_name(name):
    '''
    Make sure name is valid
    '''
    if len(name) < 1 or len(name) > 50:
        raise InputError("Input 6")
    if re.search("^[a-zA-Z]+[a-zA-Z]$", name) is None:
        raise InputError("Input 7")


def check_email(email):
    '''
    Check if email exist
    '''
    for i in range(len(data["users"])):
        if data["users"][i]["email"] == email:
            return True
    return False


def logout_state(token):
    '''
    Change state when logging in and out
    '''
    user_id = decode_token(token)
    for i in range(len(data["users"])):
        if data["users"][i]["u_id"] == user_id:
            if data["users"][i]['state'] != "active":
                raise AccessError("Access 1")
            data["users"][i]['state'] = "inactive"
