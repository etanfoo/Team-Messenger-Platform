from error import InputError
import re


def auth_login(email, password):
    emailPattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"

    if len(email) > 254:
        raise InputError(InputError)
    if len(email) == 0 or len(password) == 0:
        raise InputError(InputError)
    if re.search(emailPattern, email) == None:
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
    return {
        'u_id': 1,
        'token': '12345',
    }
