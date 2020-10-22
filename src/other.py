from global_dic import data
from error import InputError
from utils import check_token

def clear():
    data["users"].clear()
    data["channels"].clear()


def users_all(token):
    '''
    valid_token(token)
    '''
    check = check_token(token)
    if check == False:
        raise InputError
    
    authorised_users = []

    # Unable to iterate through multiple users.
    # try:
    
    for user in data["users"]:
        # for u_id in data["users"]:
        authorised_users.append({"u_id": user["u_id"], "email": user["email"], "first_name": user["first_name"], "last_name": user["last_name"]})
            # authorised_users.append({"u_id": user["u_id"], "email": user["email"], "first_name": user["first_name"], "last_name": user["last_name"], "status": user["status"]})

    return {"users": authorised_users}

    # except KeyError:
    #     raise InputError

    # return {
    #     'users': [
    #         {
    #             'u_id': 1,
    #             'email': 'cs1531@cse.unsw.edu.au',
    #             'name_first': 'Hayden',
    #             'name_last': 'Jacobs',
    #             'handle_str': 'hjacobs',
    #         },
    #     ],
    # } 


def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    
    result = []

    for channel in data["channels"]:
        if token == channel["all_members"]:
            for message in channel["messages"]:
                if query_str in message['messages']:
                    result.append(message)

    sorted(result, key=lambda message: message["time_created"], reverse = True)

    return {"messages": result}

    # return {
    #     'messages': [{
    #         'message_id': 1,
    #         'u_id': 1,
    #         'message': 'Hello world',
    #         'time_created': 1582426789,
    #     }],
    # }