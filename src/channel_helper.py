'''
Channel Helper
'''
from global_dic import data


def check_channel(channel_id):
    '''
    Check if channel exist
    '''
    global data
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return True
    return False


def check_owner(channel_id, u_id_match):
    '''
    Check if channel owner is true
    '''
    global data
    # loop through each channel
    for channel in data['channels']:
        # check channel_id exists
        if channel_id == channel['channel_id']:
            # loop through owners in that specific channel
            for owners in channel["owner_members"]:
                # check if that owner is already an owner
                if owners["u_id"] == u_id_match:
                    return True
    return False


def channel_details_helper(channel_id):
    '''
    Grab channel given by channel_id
    '''
    global data
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel


def check_uid(u_id):
    '''
    Check if u_id is valid
    '''
    global data
    for user in data['users']:
        if u_id == user['u_id']:
            return True
    return False


def check_member_channel(channel_id, u_id):
    '''
    Check if member is part of that channel
    '''
    global data
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if u_id == member['u_id']:
                    return True
    return False


def check_start(channel_id, start):
    '''
    Check Start
    '''
    global data
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if start > len(channel['messages']):
                return True
    return False


def delete_member(u_id, channel_id):
    '''
    Delete member base on user id
    '''
    global data
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for i in range(0, len(channel['all_members'])):
                if u_id == channel['all_members'][i]['u_id']:
                    del channel['all_members'][i]


def delete_owner(u_id, channel_id):
    '''
    Delete owner base on user id
    '''
    global data
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for i in range(0, len(channel['owner_members'])):
                if u_id == channel['owner_members'][i]['u_id']:
                    del channel['owner_members'][i]


def add_user(channel_id, u_id):
    '''
    Add user to the channel
    '''
    global data
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            new_user = {'u_id': u_id}
            channel['all_members'].append(new_user)


def add_owner(channel_id, uid):
    '''
    Add owner to the channel
    '''
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            new_owner = {'u_id': uid}
            channel["owner_members"].append(new_owner)


def delete_user(channel_id, u_id):
    '''
    Delete user from the channel
    '''
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['owner_members']:
                if member['u_id'] == u_id:
                    channel['owner_members'].remove(member)
                    return True
    return False