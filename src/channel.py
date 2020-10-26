'''
Channel
'''
from channel_helper import check_channel, check_uid, check_member_channel, channel_details_helper, check_start, delete_member, delete_owner, add_user, check_owner, delete_user, add_owner
from error import InputError, AccessError
from global_dic import data
from utils import decode_token, check_token


def channel_invite(token, channel_id, u_id):
    '''
    Invite user to channel
    '''
    # looping to see if channel_id is listed, if not, input error
    if check_channel(channel_id) is False:
        raise InputError

    # looping to see if u_id is a valid user, if not, input error
    if check_uid(u_id) is False:
        raise InputError

    matching_u_id = decode_token(token)

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    if check_member_channel(channel_id, matching_u_id) is False:
        raise AccessError

    # no errors raised, add the user to channels all members
    add_user(channel_id, u_id)


def channel_details(token, channel_id):
    '''
    Grab channel details
    '''
    # looping to see if channel_id is listed, if not, input error
    if check_channel(channel_id) is False:
        raise InputError
    matching_u_id = decode_token(token)

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    if check_member_channel(channel_id, matching_u_id) is False:
        raise AccessError

    return channel_details_helper(channel_id)

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
    '''
    Grab channel messages
    '''
    # looping to see if channel_id is listed, if not, input error
    if check_channel(channel_id) is False:
        raise InputError

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    # comparing token with u_id right now for iteration 1
    u_id = decode_token(token)
    if check_member_channel(channel_id, u_id) is False:
        raise AccessError

    # seeing if start is greater than total number of messages in the channel
    if check_start(channel_id, start) is True:
        raise InputError

    messages = []
    # channel_id is the index based on order created so it will be corresponding list index in data
    remaining_length = len(data['channels'][channel_id]['messages']) - start

    # determining if there are >= 50 messages left to return, if not end point is -1
    # setting last index variable for loop boundary
    if remaining_length < 50:
        end = -1
        last_index = start + remaining_length
    else:
        end = start + 50
        last_index = end

    maximum_index = len(data['channels'][channel_id]['messages']) - 1

    # looping through data structure and populating list with all messages required
    for i in range(start, last_index):
        messages.append(
            data['channels'][channel_id]['messages'][maximum_index - i])

    # print(len(messages))
    # print((messages))
    return {
        'messages': messages,
        'start': start,
        'end': end,
    }


def channel_leave(token, channel_id):
    '''
    Leave channel
    '''
    # looping to see if channel_id is listed, if not, input error
    if check_channel(channel_id) is False:
        raise InputError

    matching_u_id = decode_token(token)

    # if user is not a member of channel with channel_id, access error
    # channel is already selected on channel with channel_id (from first for loop)
    if check_member_channel(channel_id, matching_u_id) is False:
        raise AccessError

    # deleting member from channels all_members
    delete_member(matching_u_id, channel_id)

    # deleting from owner_members if an owner
    delete_owner(matching_u_id, channel_id)


def channel_join(token, channel_id):
    '''
    arg: token, channe_id
    return: nothing
 
    Given a channel_id of a channel that the authorised user can join, 
    adds them to that channel
    '''
    # looping to see if channel_id is listed, if not, InputError
    if check_channel(channel_id) is False:
        raise InputError

    check_token(token)
    # # if channel is private -> AccessError
    pub = False

    # utilizes a diff globalDict
    for channel in data['channels']:
        if channel['channel_id'] is channel_id and channel['is_public'] == True:
            pub = True
            break
    if pub is False:
        raise AccessError

    matching_u_id = decode_token(token)

    # add user to the channel
    # loop through each property of all channel

    add_user(channel_id, matching_u_id)


def channel_addowner(token, channel_id, u_id):
    '''
    Add owner to channel
    '''
    # looping to see if channel_id is listed, if not, InputError
    matching_u_id = decode_token(token)
    if check_channel(channel_id) is False:
        raise InputError
    # check if that owner is already an owner
    if check_owner(channel_id, u_id) is True:
        raise InputError

    # check if the requester is an owner of the channel
    if check_owner(channel_id, matching_u_id) is False:
        raise AccessError

    add_owner(channel_id, u_id)


def channel_removeowner(token, channel_id, u_id):
    '''
    Remove owner from channel
    '''
    matching_u_id = decode_token(token)
    if check_channel(channel_id) is False:
        raise InputError
    # check if that owner is already an owner
    if check_owner(channel_id, u_id) is False:
        raise InputError

    # check if the requester is an owner of the channel
    if check_owner(channel_id, matching_u_id) is False:
        raise AccessError

    # find the dictionary in the owner list, and delete
    delete_user(channel_id, u_id)
