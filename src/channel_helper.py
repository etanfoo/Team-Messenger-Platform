from global_dic import data


#Check if channel exist
def check_channel(channel_id):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return True
    return False


def check_owner(channel_id, u_id):
    # loop through each channel
    for channel in data['channels']:
        # check channel_id exists
        if channel_id == channel['channel_id']:
            # loop through owners in that specific channel
            for owners in channel["owner_members"]:
                # check if that owner is already an owner
                if owners["u_id"] == u_id:
                    return True
    return False


def channel_details(channel_id):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return channel


def check_channel_state(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id and channel['is_public'] == True:
            return True
    return False


#Check if u_id is valid
def check_uid(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return True
    return False


def check_member_channel(channel_id, u_id):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if u_id == channel["all_members"]:
                return True
    return False


def check_start(channel_id, start):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if start > len(channel['messages']):
                return True
    return False


def delete_member(u_id):
    for channel in data['channels']:
        for i in range(0, len(channel['all_members'])):
            if u_id == channel['all_members'][i]['u_id']:
                del channel['all_members'][i]


def delete_owner(u_id):
    for channel in data['channels']:
        for i in range(0, len(channel['owner_members'])):
            if u_id == channel['owner_members'][i]['u_id']:
                del channel['owner_members'][i]


def add_user(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            new_user = {'u_id': u_id}
            channel['all_members'].append(new_user)


def delete_user(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['owner_members']:
                if member['u_id'] == u_id:
                    channel['owner_members'].remove(member)
                    return True
    return False