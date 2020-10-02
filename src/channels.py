from global_dic import data
import channel
from error import InputError

def channels_list(token):
    authorised_channels = []
    # Loops through all channels
    for channels in data["channels"]:
        # Loops through all members of that channel
        for members in channels["all_members"]:
            # Checks if user is part of this channel
            if members["u_id"] == token:
                # Add details to the authorised_channels list
                authorised_channels.append({"channel_id": channels["channel_id"], "name": channels["name"]})
                # Speed up the search efficiency, by iterating to the next channel after being added to the list
                break
    return {'channels': authorised_channels}

def channels_listall(token):
    authorised_channels = []
    # Loops through all channels
    for channels in data["channels"]:
        # Loops through all members of that channel
        for members in channels["all_members"]:
            # Checks if the channel is public or user is part of this channel
            if channels["is_public"] == True or members["u_id"] == token:
                # Add details to the authorised_channels list
                authorised_channels.append({"channel_id": channels["channel_id"], "name": channels["name"]})
                # Prevent duplicates by breaking out of the loop once details have been added
                break
    return {'channels': authorised_channels}

def channels_create(token, name, is_public):
    # Name is over 20 characters long or empty or space => input error
    if len(name) > 20 or name == '' or name.isspace():
        raise InputError
    # The next available id
    available_id = len(data["channels"])
    # Form the data structure
    data["channels"].append({"name": name, "channel_id": available_id, "is_public": is_public, "owner_members": [{"u_id": token}], "all_members": [{"u_id": token}]})
    # Token == u_id for now
    return {'channel_id': available_id}
