'''
Channel
'''
from global_dic import data
from error import InputError
from utils import decode_token, check_token
from channels_helper import valid_channel_name


###################
# channels function
###################
def channels_list(token):
    ''' 
    Loops through the list of channels and each member in that channel,
    checking if the current user is part of that channel. If so, add
    the channel details to the authorized_channels list. 
    
    Return: a list of channels the user is part of
    '''
    check_token(token)

    u_id = decode_token(token)
    authorized_channels = []
    # Loops through all channels
    for channels in data["channels"]:
        # Loops through all members of that channel
        for members in channels["all_members"]:
            # Checks if user is part of this channel
            if members["u_id"] == u_id:
                # Add details to the authorized_channels list
                authorized_channels.append({
                    "channel_id": channels["channel_id"],
                    "name": channels["name"]
                })
                # Speed up the search efficiency, by iterating to the next channel after being added to the list
                break
    return {'channels': authorized_channels}


def channels_listall(token):
    ''' 
    Adds all public channels and loops through the list private 
    of channels, checking if the current user is part of that channel. If so, add
    the channel details to the authorized_channels list. 

    Return: a list of all public channels and any private channels the user is part of
    '''
    check_token(token)

    u_id = decode_token(token)
    authorized_channels = []
    # Loops through all channels
    for channels in data["channels"]:
        if channels['is_public'] == True:
            authorized_channels.append({
                "channel_id": channels["channel_id"],
                "name": channels["name"]
            })
        else:
            # Loops through all members of that channel
            for members in channels["all_members"]:
                # Checks if the channel is public or user is part of this channel
                if members["u_id"] == u_id:
                    # Add details to the authorised_channels list
                    authorized_channels.append({
                        "channel_id":
                        channels["channel_id"],
                        "name":
                        channels["name"]
                    })
                    # Prevent duplicates by breaking out of the loop once details have been added
                    break
    return {'channels': authorized_channels}


def channels_create(token, name, is_public):
    ''' 
    Create a public/private channel with a given name, and add the current user’s details to “owner_members” and “all_members”
    Return: the channel_id
    '''
    check_token(token)

    u_id = decode_token(token)
    # Name is over 20 characters long or empty or space => input error
    valid_channel_name(name)
    # The next available id
    available_id = len(data["channels"])

    # obtaining the correct user and assigning it to variable person
    for user in data["users"]:
        if token == user["token"]:
            person = user
            break

    # creating a list of owners that will have global permissions across all channels
    list_of_owners = []

    for user in data['users']:
        if user['is_flockr_owner']:
            list_of_owners.append(user)


    # Form the data structure
    data["channels"].append({
        "name":
        name,
        "channel_id":
        available_id,
        "is_public":
        is_public,
        "owner_members": [{
            "u_id": u_id,
            "name_first": person["first_name"],
            "name_last": person["last_name"]
        }],
        "all_members": [{
            "u_id": u_id,
            "name_first": person["first_name"],
            "name_last": person["last_name"]
        }],
        "messages": [],
        "standup": [],
    })

    # grabbing channel we just created
    for channel in data['channels']:
        if channel['channel_id'] == available_id:
            new_channel = channel

    # adding all flockr owners as members to channel
    for owner in list_of_owners:
        user_info = {'u_id': owner['u_id'], 'name_first': owner['first_name'], 'name_last': owner['last_name']}
        new_channel['owner_members'].append(user_info)
        new_channel['all_members'].append(user_info)


    return {'channel_id': available_id}
