from global_dic import data

# import channel
from error import InputError
from utils import decode_token
from channels_helper import valid_channel_name


###################
# channels function
###################
def channels_list(token):
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
    u_id = decode_token(token)
    authorized_channels = []
    # Loops through all channels
    for channels in data["channels"]:
        # Loops through all members of that channel
        for members in channels["all_members"]:
            # Checks if the channel is public or user is part of this channel
            if channels["is_public"] == True or members["u_id"] == u_id:
                # Add details to the authorised_channels list
                authorized_channels.append({
                    "channel_id": channels["channel_id"],
                    "name": channels["name"]
                })
                # Prevent duplicates by breaking out of the loop once details have been added
                break
    return {'channels': authorized_channels}


def channels_create(token, name, is_public):
    u_id = decode_token(token)
    # Name is over 20 characters long or empty or space => input error
    valid_channel_name(name)
    # The next available id
    available_id = len(data["channels"])
    # Form the data structure
    data["channels"].append({
        "name": name,
        "channel_id": available_id,
        "is_public": is_public,
        "owner_members": [{
            "u_id": u_id
        }],
        "all_members": [{
            "u_id": u_id
        }]
    })
    return {'channel_id': available_id}
