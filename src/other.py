'''
other.py contains the clear, users_all, admin_permission_change, and search functions
'''
from global_dic import data
from error import InputError, AccessError
from utils import check_token, decode_token
from channels import channels_list
from channel_helper import check_uid

def clear():
    '''
    Function to reset user and channel entries in the data dictionary
    '''
    data["users"].clear()
    data["channels"].clear()
    data["standup"].clear()
    data["message_count"] = 0


def users_all(token):
    '''
    Function which returns a list of all the users
    '''
    # Check if user's token is valid
    check_token(token)

    # List of authorised users
    authorised_users = []

    # Gather user details and append list
    for user in data["users"]:
        authorised_users.append({
            "u_id": user["u_id"],
            "email": user["email"],
            "name_first": user["first_name"],
            "name_last": user["last_name"],
            'handle_str': user['handle'],
            'profile_img_url': user['profile_img_url']
        })

    # Return list as dictionary
    return {"users": authorised_users}


def admin_userpermission_change(token, u_id, permission_id):
    '''
    Function to alter a user's permission to an owner, or from an owner to a member
    '''
    global data
    # Error checks
    check_token(token)
    if check_uid(u_id) is False:
        raise InputError("Not valid user")

    if permission_id not in [1, 2]:
        raise InputError("Not a valid permission value")

    for user in data['users']:
        if user['token'] == token:
            if user['is_flockr_owner'] == False:
                raise InputError("You are not an owner of Flockr")
            break

    # changing permissions to new permissions
    new_permission = permission_id == 1

    for user in data['users']:
        if user['u_id'] == u_id:
            user['is_flockr_owner'] = new_permission
            user_details = {
                'u_id': u_id, 
                'name_first': user['first_name'], 
                'name_last': user['last_name']
            }

    for channel in data['channels']:
        is_member = False
        for member in channel["owner_members"]:
            if member['u_id'] == u_id:
                is_member = True
        if is_member == False:
            channel["owner_members"].append(user_details)
        is_member = False
        for member in channel["all_members"]:
            if member['u_id'] == u_id:
                is_member = True
        if is_member == False:
            channel["all_members"].append(user_details)

    return {}


    


def search(token, query_str):
    '''
    Function to search for previous messages
    '''

    user_channels = []

    user_u_id = decode_token(token)

    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == user_u_id:
                user_channels.append(channel)

    result = []

    # Search for query in the channel's message history
    for channel in user_channels:
        for message in channel["messages"]:
            if query_str in message['message']:
                result.append(message)

    # Sort list based on time_created
    sorted(result, key=lambda message: message["time_created"], reverse=True)

    # Return dictionary containing result list
    return {"messages": result}
