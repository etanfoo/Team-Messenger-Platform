'''
Message Helper
'''
from error import InputError, AccessError
from global_dic import data


def get_message(message_id):
    """
    Get the corresponding message by message_id
    """
    for channel in data["channels"]:
        for message in channel["messages"]:
            if (message["message_id"] == message_id):
                return message
    raise InputError("Message_ID does not exist")


def get_channel(message_id):
    """
    Get the corresponding channel by message_id
    """
    for channel in data["channels"]:
        for message in channel["messages"]:
            if (message["message_id"] == message_id):
                return channel
    raise InputError("Channel does not exist")


def get_message_owner(message_id):
    """
    Get the user_id with the corresponding message_id
    """
    for channel in data["channels"]:
        for message in channel["messages"]:
            if (message["message_id"] == message_id):
                return message["u_id"]
    raise InputError("Message owner does not exist")


def valid_message(message):
    """
    Check if the message length is valid
    """
    if (len(message) > 1000):
        raise InputError(
            description=
            'Your message should be less than 1000 characters and at least 1 character'
        )