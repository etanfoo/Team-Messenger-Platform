from error import InputError, AccessError
import jwt
from appsecret import JWT_SECRET
from global_dic import data
from utils import decode_token
import datetime


def message_send(token, channel_id, message):
    if (len(message) > 1000):
        raise InputError(
            description=
            'Your message should be less than 1000 characters and at least 1 character'
        )
    user_id = decode_token(token)
    #Check if channel_id is valid
    #check if user is a member of that channel
    data["channels"]["messages"].append({
        "u_id": decode_token("user_id"),
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
