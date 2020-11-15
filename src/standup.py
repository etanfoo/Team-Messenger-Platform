'''
standup functionality.
once standups are finished, all messages sent to standup/send are packaged together in a single messaged
and posted by the user who begun the standup/
'''
from global_dic import data
from threading import Timer
from datetime import datetime
from error import InputError, AccessError
from utils import check_token, decode_token, get_current_timestamp
from channel_helper import check_channel, check_member_channel


def standup_active(token, channel_id):
    '''
    Function which checks if standup is active
    will return a timestamp of when standup will finish
    '''
    # check if user's token is valid
    check_token(token)

    # check if channel_id is valid
    if check_channel(channel_id) is False:
        raise InputError("Input error as channel_id is not valid")

    # check if standup is active already
    # get standup from dict and check channel_id

    is_active = False
    time_finish = 0
    for channel in data["standup"]:
        if channel_id == channel["channel_id"]:
            time_finish = channel["time_finish"]
    if time_finish - get_current_timestamp() > 0:
        is_active = True

    if is_active:
        return {'is_active': is_active, 'time_finish': time_finish}
    else:
        data['standup'] = []
        return {'is_active': is_active, 'time_finish': None}

def standup_end(token, channel_id):
    '''
    sends the messages that have been accumulated
    '''

    new_message = ''
    for i in range(0, len(data['standup'][0]['messages'])):
        new_message += data['standup'][channel_id]['messages'][i]['handle'] + ': ' + data['standup'][channel_id]['messages'][i]['message'] + '\n' 
 
    data["message_count"] += 1

    u_id = decode_token(token)

    #Append message to dictionary
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["messages"].append({
                'u_id': u_id,
                'message_id': data["message_count"],
                'time_created': get_current_timestamp(),
                'message': new_message,
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            })
    
    # print(f'THIS IS GLOBAL DATA {data}')

def standup_start(token, channel_id, length):
    '''
    Function which starts standup
    '''
    # check if user's token is valid
    check_token(token)

    # check if channel_id is valid
    if check_channel(channel_id) is False:
        raise InputError("Input error as channel_id is not valid")

    if length <= 0:
        raise InputError("Input error standup length is too short")

    # check if standup is active already
    if standup_active(token, channel_id)['is_active'] == True:
        raise InputError("Input error as standup is already active")

    print(f'TIME START: {get_current_timestamp()}')

    time_finish = int(get_current_timestamp() + length)
    data["standup"].append({
        "channel_id": channel_id,
        "messages": [],
        "time_finish": time_finish,
    })
    standup = Timer(length, standup_end, args=[token, channel_id])
    standup.start()

    
    print(f'TIME FINISH: {time_finish}')
    return {'time_finish': time_finish}


def standup_send(token, channel_id, message):
    '''
    Function which sends message during standup
    '''
    # check if user's token is valid
    check_token(token)
    # decode token and get u_id
    u_id = decode_token(token)

    # check if channel_id is valid
    if check_channel(channel_id) is False:
        raise InputError("Input error as channel_id is not valid")
    if check_member_channel(channel_id, u_id) is False:
        raise AccessError("Not a member")
    # check if message is over 1000 characters long
    if len(message) > 1000:
        raise InputError("Input error message too long")

    # Check if standup is active
    # if not active then inputerror
    # check if standup is active already
    check_standup = standup_active(token, channel_id)
    if check_standup['is_active'] == False:
        raise InputError("Input error as standup is not active")

    for user in data['users']:
        if user['token'] == token:
            handle = user['handle']

    for channel in data["standup"]:
        if channel["channel_id"] == channel_id:
            channel["messages"].append({'message': message, 'handle': handle})

    return {}