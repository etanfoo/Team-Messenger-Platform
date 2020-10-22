import re
import hashlib
from error import InputError, AccessError
from global_dic import data

#This function check that inputs are email is valid according to project specifications
#Function for auth login and auth register


#Validate Email
def validate_email(email):
    emailPattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    #Email length less than 255
    if len(email) > 254:
        raise InputError(InputError)
    #Email length must be more than 0
    if len(email) == 0:
        raise InputError(InputError)
    if re.search(emailPattern, email) == None:
        raise InputError(InputError)


def validate_password(password):
    if len(password) < 6:
        raise InputError(InputError)
    if len(password) > 18:
        raise InputError(InputError)


def hash_password(password):
    return hashlib.sha256(str(password).encode('utf-8')).hexdigest()


def validate_name(name):
    if len(name) < 1 or len(name) > 50:
        raise InputError(InputError)
    if (re.search("^[a-zA-Z]+[a-zA-Z]$", name) == None):
        raise InputError(InputError)


def check_email(email):
    for i in range(len(data["users"])):
        if (data["users"][i]["email"] == email):
            return True
    return False


def logout_state(token):
    for i in range(len(data["users"])):
        if (data["users"][i]["token"] == token):
            if (data["users"][i]['state'] != "active"):
                raise AccessError(AccessError)
            data["users"][i]['state'] = "inactive"