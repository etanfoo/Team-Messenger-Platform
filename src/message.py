"""
MESSAGE
"""
import datetime
from error import InputError, AccessError
from global_dic import data
from utils import decode_token, check_token
from message_helper import get_message, get_message_owner, valid_message
from channel_helper import check_member_channel, check_channel


def message_send(token, channel_id, message):
    """
    Function that sends a message to the provided channel_id
    """
    #Check if message is valid
    valid_message(message)
    #Check if token is valid
    check_token(token)
    #Decode token
    u_id = decode_token(token)
    #Check if the channel exist
    if check_channel(channel_id) is False:
        raise InputError
    #Check if the user is authorized in the channel
    if check_member_channel(channel_id, u_id) is False:
        raise AccessError
    #Increment the message counter by 1
    data["message_count"] += 1
    #Append message to dictionary
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["messages"].append({
                "u_id":
                u_id,
                "message_id":
                data["message_count"],
                "message":
                message,
                "time_created":
                datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            })
    return {
        'message_id': data["message_count"],
    }


def message_remove(token, message_id):
    """
    Function that removes message given message_id
    """
    #Make sure token is valid
    check_token(token)
    # #Decode the token to user ID
    u_id = decode_token(token)
    #Check if message_id exist
    get_message(message_id)
    #Check if user_id belongs to the message_id
    if u_id != get_message_owner(message_id):
        raise AccessError(AccessError)
    for channel in data["channels"]:
        for i in range(len(channel["messages"])):
            if channel["messages"][i]["message_id"] == message_id:
                del channel["messages"][i]
                return
    return {}


def message_edit(token, message_id, message):
    """
    Function that edits the message
    """
    #Message cannot be longer than 1000 characters
    valid_message(message)
    #Check if message_id exist
    get_message(message_id)
    #Check if token is valid
    check_token(token)
    #Get user_id from token
    u_id = decode_token(token)
    #Check if user is authorized to edit
    if u_id != get_message_owner(message_id):
        raise AccessError(AccessError)
    #Remove message if the message size is 0
    if len(message) == 0:
        message_remove(token, message_id)
        return {}
    for channel in data["channels"]:
        for i in range(len(channel["messages"])):
            if channel["messages"][i]["message_id"] == message_id:
                channel['messages'][i]["message"] = message
    return {}
