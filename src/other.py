'''
other.py contains the clear, users_all, admin_permission_change, and search functions
'''
from global_dic import data
from error import InputError, AccessError
from utils import check_token, decode_token

def clear():
    '''
    Function to reset user and channel entries in the data dictionary
    '''
    data["users"].clear()
    data["channels"].clear()


def users_all(token):
    '''
    Function which returns a list of all the users
    '''
    # Check if user's token is valid
    check = check_token(token)
    if check == False:
        raise AccessError
    
    # List of authorised users
    authorised_users = []
    
    # Gather user details and append list
    for user in data["users"]:
        authorised_users.append({
            "u_id": user["u_id"], 
            "email": user["email"], 
            "first_name": user["first_name"], 
            "last_name": user["last_name"]
        })

    # Return list as dictionary
    return {"users": authorised_users}

def admin_userpermission_change(token, u_id, permission_id): 
    '''
    Function to alter a user's permission to an owner, or from an owner to a member
    '''   

    # Check for valid token
    check = check_token(token)
    if check == False:
        raise AccessError
    token_id = decode_token(token)

    # Check for self demotion/promotion
    if token_id == u_id:
        raise AccessError

    # Check for empty u_id
    if u_id == '':
        raise InputError

    # Check for invalid permission_id type
    if type(permission_id) == str:
        raise InputError

    # Check if permission_id's are valid inputs
    if permission_id != 1:
        if permission_id != 2:
            raise InputError

    # Check if permission_id is not empty
    if permission_id == None:
        raise InputError

    # Check if u_id exists in the channel
    user_check = False
    for channels in data["channels"]:
        for users in channels["all_members"]:
            if u_id == users["u_id"]:
                user_check = True
    if user_check == False:
        raise InputError

    # Check if person is a owner with perms
    owner_check = False
    for channels in data["channels"]:
        for owners in channels["owner_members"]:
            if token_id == owners["u_id"]:
                owner_check = True
    if owner_check == False:
        raise AccessError

    # Depending on permission_id, either promote or demote user
    if permission_id == 1:
        # 1, Promote user to admin
        completed = False
        for promotion in data["channels"]:
            if completed == False:
                promotion["owner_members"].append({"u_id": u_id})
                completed = True

    elif permission_id == 2:
        # 2, Demote user to member
        for demotion in data["channels"]:
            for demotion_id in demotion["owner_members"]:
                if demotion_id["u_id"] == u_id:
                    demotion["owner_members"].remove({"u_id": u_id})
                  
    return 0 

def search(token, query_str):
    '''
    Function to search for previous messages
    '''
    # Check for valid token
    check = check_token(token)
    if check == False:
        raise AccessError

    # Check if query_str is not empty
    if query_str == None:
        raise InputError

    result = []
    # Search for query in the channel's message history
    for channel in data["channels"]:
        for message in channel["messages"]:
            if query_str in message['message']:
                result.append(message)

    # Sort list based on time_created
    sorted(result, key=lambda message: message["time_created"], reverse=True)

    # Return dictionary containing result list
    return {"messages": result}
