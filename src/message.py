from error import InputError, AccessError
import jwt
from appsecret import JWT_SECRET
from global_dic import data
import datetime


def message_send(token, channel_id, message):
    if (len(message) > 1000):
        raise InputError(InputError)
    data["channels"]["messages"].append({
        "u_id": decoded["user_id"],
        "message_id": 3,
        "message": message,
        "time_created": datetime.now(),
    })
    return {
        'message_id': 1,
    }


def message_remove(token, message_id):

    return {}


def message_edit(token, message_id, message):
    if (len(message) > 1000):
        raise InputError(InputError)

    return {}
