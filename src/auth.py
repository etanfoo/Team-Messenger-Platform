from error import InputError
from global_dic import data
import uuid
import re


def auth_login(email, password):
    find = False
    emailPattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    if len(email) > 254:
        raise InputError(InputError)
    if len(email) == 0 or len(password) == 0:
        raise InputError(InputError)
    if re.search(emailPattern, email) == None:
        raise InputError(InputError)
    for i in range(len(data["users"])):
        if (data["users"][i]["email"] == email):
            find = True
            if (data["users"][i]["password"] != password):
                raise InputError(InputError)
            else:
                data["users"][i]["status"] = "active"
    if find == False:
        raise InputError(InputError)
    return {
        'u_id': 1,
        'token': '12345',
    }


def auth_logout(token):
    return {
        'is_success': True,
    }


def auth_register(email, password, name_first, name_last):
    emailPattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    if re.search(emailPattern, email) == None:
        raise InputError(InputError)
    if len(email) > 254:
        raise InputError(InputError)
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
    data["users"].append({
        "u_id": uuid.uuid4().hex,
        "email": email,
        "first_name": name_first,
        "last_name": name_last,
        "status": "inactive",
        "password": password
    })

    return {
        'u_id': 1,
        'token': '12345',
    }
