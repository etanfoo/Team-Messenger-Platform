from global_dic import data
from channel import *
from error import InputError

def channels_list(token):
    authorised_channels = []
    # Loops through all channels
    for channels in data["channels"]:
        # Loops through the all members of that channel
        for members in channels["all_members"]:
            # Token == u_id for now
            # User is part of this channel
            if members["u_id"] == token:
                # Add channel_id and channel_name to authorised_channels
                authorised_channels.append({"channel_id": channels["channel_id"], "name": channels["name"],})
    return {'channels': authorised_channels}

def channels_listall(token):
    channel_list = []
    # Loops through all channels
    for channels in data["channels"]:
        # Add channel_id and channel_name to channel_list
        channel_list.append({"channel_id": channels["channel_id"], "name": channels["name"]})    
    # Potential bug - Don't know how to separate each dictionary with , 
    return {'channels': channel_list}

def channels_create(token, name, is_public):
    # Name is over 20 characters long => input error
    if len(name) > 20 or name == '' or name == ' ':
        raise InputError
    # Counter that increments to the next available channel_id
    id_counter = 0
    # Loops through all channels 
    for i in range(len(data["channels"])):
        id_counter += 1
    data["channels"].append({"channel_id": id_counter, "name": name, "all_members": [{"u_id": token}]})
    # Token == u_id for now
    channel_addowner(token, id_counter, token)
    return {'channel_id': id_counter}
