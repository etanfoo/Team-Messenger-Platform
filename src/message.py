from error import InputError, AccessError
import jwt
from appsecret import JWT_SECRET
from global_dic import data, num_messages
from utils import decode_token, check_token
from channel_helper import check_member_channel, check_channel
import datetime


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
    for channel in data["channels"]:
        for message in channel["messages"]:
            if (message["message_id"] == message_id):
                return message["u_id"]
    raise InputError("Message owner does not exist")


def message_send(token, channel_id, message):
    if (len(message) > 1000):
        raise InputError(
            description=
            'Your message should be less than 1000 characters and at least 1 character'
        )
#     #---------------------
#     # check_token(token)
#     # #Check if channel_id is valid
#     # u_id = decode_token(token)
#     #----------------------------
    u_id = token
    #Check if the channel exist
    check_channel(channel_id)
    #Check if the user is authorized in the channel
    if (check_member_channel(channel_id, u_id) == False):
        raise AccessError


#     # num_messages += 1
#     #check if user is a member of that channel
#     # for channel in data["channels"]:
#     #     if channel["channel_id"] == channel_id:
#     #         channel["messages"].append({
#     #             "u_id":
#     #             u_id,
#     #             "message_id":
#     #             num_messages,
#     #             "message":
#     #             message,
#     #             "time_created":
#     #             datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
#     #         })
    return {
        'message_id': 1,
    }


def message_remove(token, message_id):
    check_token(token)
    u_id = decode_token(token)
    find = False
    for channel in data['channels']:
        for i in range(0, len(channel['messages'])):
            if u_id == channel['messages'][i]['message_id']:
                del channel['messages'][i]
                find = True
    if (find == False):
        raise InputError(InputError)


def message_edit(token, message_id, message):
    if (len(message) > 1000):
        raise InputError(InputError)
    check_token(token)
    u_id = decode_token(token)
    #Remove message if the message size is 0
    if (len(message) == 0):
        message_remove(token, message_id)
    find = False
    for channel in data['channels']:
        for i in range(0, len(channel['messages'])):
            if u_id == channel['messages'][i]['message_id']:
                channel['messages'][i]["message"] = message
                find = True
    if (find == False):
        raise InputError(InputError)


if __name__ == '__main__':
    message_send(1, 1, "hi")
    print(get_message_owner(1))
    #print(data)