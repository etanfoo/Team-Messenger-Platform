'''
AUTH_HELPER FUNCTION
'''
import re
import hashlib
from error import InputError, AccessError
from global_dic import data
from utils import decode_token
import random
import string

#Validate Email
def validate_email(email):
    '''
    Make sure email is valid
    '''
    e_pattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    #Email length less than 255
    if len(email) > 254:
        raise InputError("Input Error")
    #Email length must be more than 0
    if len(email) == 0:
        raise InputError("Input Error")
    if re.search(e_pattern, email) is None:
        raise InputError("Input Error")


def validate_password(password):
    '''
    Make sure password comply
    '''
    if len(password) < 6:
        raise InputError("Input Error")
    if len(password) > 18:
        raise InputError("Input Error")


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
        raise InputError("Name Length")
    # if re.search("^[a-zA-Z]+[a-zA-Z]$", name) is None:
    #     raise InputError("IDK")


def check_email(email):
    '''
    Check if email exist
    '''
    for i in range(len(data["users"])):
        if data["users"][i]["email"] == email:
            return True
    return False

def check_unique_handle(handle):
    # checking if handle is already in use
    for user in data['users']:
        if handle == user['handle']:
            return False
    return True

def change_handle(handle):
    # checking if handle is greater than 20 chars
    if len(handle) > 20:
        handle = handle[0:20]

    letters = string.ascii_lowercase

    while check_unique_handle(handle) is False or len(handle) < 3:
        handle = ''.join(random.choice(letters) for i in range(20))
    return handle
        