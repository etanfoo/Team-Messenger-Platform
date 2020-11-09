"""
MESSAGE
"""
import datetime
from threading import Timer
from error import InputError, AccessError
from global_dic import data
from utils import decode_token, check_token, get_current_timestamp
from message_helper import get_channel, get_message, get_message_owner, valid_message
from channel_helper import check_member_channel, check_channel, check_owner

VALID_REACTS = [1]


def message_send(token, channel_id, message):
    """
    Function that sends a message to the provided channel_id
    """
    global data
    #Check if message is valid
    valid_message(message)
    # #Check if token is valid
    check_token(token)
    #Decode token
    u_id = decode_token(token)
    #Check if the channel exist
    if check_channel(channel_id) is False:
        raise InputError("Input error")
    #Check if the user is authorized in the channel
    if check_member_channel(channel_id, u_id) is False:
        raise AccessError("Access error")
    #Increment the message counter by 1
    data["message_count"] += 1
    #Append message to dictionary
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["messages"].append({
                'u_id':
                u_id,
                'message_id':
                data["message_count"],
                'time_created':
                get_current_timestamp(),
                'message':
                message,
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned':
                False
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


def create_message(user_id, message_id, time_created, message):
    '''
    returns a default message with is_pinned = False
    '''
    return {
        'u_id':
        user_id,
        'message_id':
        message_id,
        'time_created':
        time_created,
        'message':
        message,
        'reacts': [{
            'react_id': 1,
            'u_ids': [user_id],
            'is_this_user_reacted': False
        }],
        'is_pinned':
        False
    }


def message_react(token, message_id, react_id):
    '''
    adds a reaction to a messages list of reactions
    expects parameter types:
        token: str
        message_id: int
        react_id: int
    returns empty dictionary
    '''
    check_token(token)
    u_id = decode_token(token)
    channel_id = get_channel(message_id)
    message = get_message(message_id)
    if not check_member_channel(channel_id['channel_id'], u_id):
        raise AccessError(description='User is not in channel')
    if react_id not in VALID_REACTS:
        raise InputError(description='Invalid react id')
    for react in message['reacts']:
        if react['react_id'] == react_id:
            if u_id in react['u_ids']:
                raise InputError(description='Already reacted')
            react['u_ids'].append(u_id)
            react['is_this_user_reacted'] = True
    return {}


def message_unreact(token, message_id, react_id):
    '''
    removes a reaction from a messages list of reactions
    expects parameter types:
        token: str
        message_id: int
        react_id: int
    returns empty dictionary
    '''
    check_token(token)
    u_id = decode_token(token)
    message = get_message(message_id)
    channel_id = get_channel(message_id)
    if react_id not in VALID_REACTS:
        raise InputError(description='Invalid react id')
    if not check_member_channel(channel_id['channel_id'], u_id):
        raise AccessError(description='User is not in channel')
    for react in message['reacts']:
        if react['react_id'] == react_id:
            if u_id in react['u_ids']:
                react['u_ids'].remove(u_id)
                react['is_this_user_reacted'] = False
            else:
                raise InputError(description='You have not made this reaction')
    return {}


def message_pin(token, message_id):
    '''
    Pins a message in a channel
    '''
    check_token(token)
    u_id = decode_token(token)
    channel_specific = get_channel(message_id)
    message_specific = get_message(message_id)
    if u_id not in channel_specific['all_members'] and not check_owner(
            u_id, channel_specific['channel_id']):
        raise AccessError(
            description=
            'The authorised user is not a member of the channel that the message is within'
        )

    if not check_owner(u_id, channel_specific['channel_id']):
        raise InputError(description='The authorised user is not an owner')

    if message_specific['is_pinned']:
        raise InputError(
            description='Message with ID message_id is already pinned')

    if check_owner(u_id, channel_specific['channel_id']
                   ) is True and message_specific['is_pinned'] is False:
        message_specific['is_pinned'] = True

    return {}


def message_unpin(token, message_id):
    '''
    Unpins a message in a channel
    '''
    check_token(token)
    u_id = decode_token(token)
    channel_specific = get_channel(message_id)
    message_specific = get_message(message_id)
    if u_id not in channel_specific['all_members'] and not check_owner(
            u_id, channel_specific['channel_id']):
        raise AccessError(
            description=
            'The authorised user is not a member of the channel that the message is within'
        )

    if not check_owner(u_id, channel_specific['channel_id']):
        raise InputError(description='The authorised user is not an owner')
    if message_specific['is_pinned'] is False:
        raise InputError(
            description='Message with ID message_id is already unpinned')
    if check_owner(u_id, channel_specific['channel_id']
                   ) is True and message_specific['is_pinned'] is True:
        message_specific['is_pinned'] = False

    return {}


def message_sendlater(token, channel_id, message, time_sent):
    '''
    sends a message at a given time_sent, where time_sent is a unix timestamp
    greater than the current time.
    '''
    check_token(token)
    u_id = decode_token(token)
    if not check_channel(channel_id):
        raise InputError(description="No channel exists with that ID")
    if not check_member_channel(channel_id, u_id):
        raise AccessError(description='You are not a member of this channel')
    if len(message) > 1000 or len(message) < 1:
        raise InputError(
            description=
            'Your message should be less than 1000 characters and at least 1 character'
        )
    current_time = get_current_timestamp()
    if current_time >= time_sent:
        raise InputError(description="You can not send a message back in time")
    delay = time_sent - current_time
    data["message_count"] += 1
    message_id = data["message_count"]
    message_template = create_message(u_id, message_id, time_sent, message)
    timer = Timer(delay, sendlater_end, args=[channel_id, message_template])
    timer.start()
    return {'message_id': message_id}


def sendlater_end(channel_id, message):
    '''
    Helper function for message_sendlater, used with threading.Timer to
    add a messsage to a channels list of message after a delay.
    '''
    global data
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["messages"].append(message)
