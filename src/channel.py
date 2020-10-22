from auth import auth_login, auth_register, auth_register
from channels import channels_list, channels_listall, channels_create
from channel_helper import check_channel, check_uid, check_member_channel, channel_details, check_start, delete_member, delete_owner, check_channel_state, add_user, check_owner, delete_user
from error import InputError, AccessError
from other import clear
from global_dic import data
from utils import decode_token


def channel_invite(token, channel_id, u_id):
    # looping to see if channel_id is listed, if not, input error
    if (check_channel(channel_id) == False):
        raise InputError

    # looping to see if u_id is a valid user, if not, input error
    if (check_uid(u_id) == False):
        raise InputError

    matching_u_id = decode_token(token)

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    if (check_member_channel(channel_id, u_id) == False):
        raise AccessError

    # no errors raised, add the user to channels all members
    new_user = {'u_id': u_id}
    channels['all_members'].append(new_user)
    return {}


def channel_details(token, channel_id):

    # looping to see if channel_id is listed, if not, input error
    if (check_channel(channel_id) == False):
        raise InputError

    matching_u_id = decode_token(token)

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    if (check_member_channel(channel_id, matching_u_id) == False):
        raise AccessError

    return channel_details(channel_id)
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
    if (check_channel(channel_id) == False):
        raise InputError

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    u_id = decode_token(token)
    if (check_member_channel(channel_id, u_id) == False):
        raise AccessError

    # seeing if start is greater than total number of messages in the channel
    if (check_start(channel_id, start) == True):
        raise InputError
    return {
        'messages': [{
            'message_id': 1,
            'u_id': 1,
            'message': 'Hello world',
            'time_created': 1582426789,
        }],
        'start':
        0,
        'end':
        50,
    }


def channel_leave(token, channel_id):

    # looping to see if channel_id is listed, if not, input error
    if (check_channel(channel_id) == False):
        raise InputError

    matching_u_id = decode_token(token)

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    if (check_member_channel(channel_id, matching_u_id) == False):
        raise AccessError

    # deleting member from channels all_members
    delete_member(matching_u_id)

    # deleting from owner_members if an owner
    delete_owner(matching_u_id)

    return {}


def channel_join(token, channel_id):
    '''
    arg: token, channe_id
    return: nothing

    Given a channel_id of a channel that the authorized user can join, 
    adds them to that channel
    '''
    # looping to see if channel_id is listed, if not, InputError
    if (check_channel(channel_id) == False):
        raise InputError

    #Check if channel is private
    if (check_channel_state(channel_id) == False):
        return AccessError

    matching_u_id = decode_token(token)

    # add user to the channel
    # loop through each property of all channe
    add_user(channel_id, matching_u_id)
    return {}


def channel_addowner(token, channel_id, u_id):
    # looping to see if channel_id is listed, if not, InputError
    alreadyOwner = False
    isAdmin = False

    matching_u_id = decode_token(token)
    if (check_channel(channel_id) == False):
        raise InputError
    # check if that owner is already an owner
    if (check_owner(channel_id, u_id) == True):
        raise InputError

    # check if the requester is an owner of the channel
    if (check_owner(channel_id, matching_u_id) == False):
        raise AccessError

    new_owner = {'u_id': u_id}
    #Add owner to channel
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel["owner_members"].append(new_owner)
    return {}


def channel_removeowner(token, channel_id, u_id):
    #Decode token
    matching_u_id = decode_token(token)
    if (check_channel(channel_id) == False):
        raise InputError

    # check if that owner is already an owner
    if (check_owner(channel_id, u_id) == True):
        raise InputError

    # check if the requester is an owner of the channel
    if (check_owner(channel_id, matching_u_id) == False):
        raise AccessError

    # find the dictionary in the owner list, and delete
    delete_user(channel_id, u_id)

    return {}
