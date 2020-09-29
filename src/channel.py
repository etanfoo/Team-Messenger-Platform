from globalDic import data
from auth import *
from channels import *
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):

    # looping to see if channel_id is listed, if not, input error
    found = False
    for channel in data['Channel']:
        if channel_id == channel['channel_id']:
            found = True
            break
    if found == False:
        raise InputError

    # looping to see if u_id is a valid user, if not, input error
    found = False
    for user in data['users']:
        if u_id == user['u_id']:
            found = True
            break
    if found == False:
        raise InputError

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    # comparing token with u_id right now for iteration 1
    found = False
    for member in channel['all_members']:
        if token == member['u_id']:
            found = True
            break
    if found == False:
        raise AccessError
    
    # no errors raised, add the user to channels all members
    new_user = {'u_id': u_id}
    channel['all_members'].append(new_user)
    return {
    }

def channel_details(token, channel_id):

    # looping to see if channel_id is listed, if not, input error
    found = False
    for channel in data['Channel']:
        if channel_id == channel['channel_id']:
            found = True
            break
    if found == False:
        raise InputError

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    # comparing token with u_id right now for iteration 1
    found = False
    for member in channel['all_members']:
        if token == member['u_id']:
            found = True
            break
    if found == False:
        raise AccessError

    return channel
    # return {
    #     'name': 'Hayden',
    #     'owner_members': [
    #         {
    #             'u_id': 1,
    #             'name_first': 'Hayden',
    #             'name_last': 'Jacobs',
    #         }
    #     ],
    #     'all_members': [
    #         {
    #             'u_id': 1,
    #             'name_first': 'Hayden',
    #             'name_last': 'Jacobs',
    #         }
    #     ],
    # }

def channel_messages(token, channel_id, start):

    # looping to see if channel_id is listed, if not, input error
    found = False
    for channel in data['Channel']:
        if channel_id == channel['channel_id']:
            found = True
            break
    if found == False:
        raise InputError

    # seeing if start is greater than total number of messages in the channel
    if start > len(channel['messages']):
        raise InputError

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    # comparing token with u_id right now for iteration 1
    found = False
    for member in channel['all_members']:
        if token == member['u_id']:
            found = True
            break
    if found == False:
        raise AccessError


    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):

    # looping to see if channel_id is listed, if not, input error
    found = False
    for channel in data['Channel']:
        if channel_id == channel['channel_id']:
            found = True
            break
    if found == False:
        raise InputError

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    # comparing token with u_id right now for iteration 1
    found = False
    for member in channel['all_members']:
        if token == member['u_id']:
            found = True
            break
    if found == False:
        raise AccessError
    
    # deleting member from channels all_members
    for member in channel['all_members']:
        if token == member['u_id']:
            member.clear()

    # deleting from owner_members if an owner
    for member in channel['owner_members']:
        if token == member['u_id']:
            member.clear()

    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }