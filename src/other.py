from global_dic import data


def clear():
    data["users"].clear()
    data["channels"].clear()


def users_all(token):
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

<<<<<<< HEAD
<<<<<<< HEAD
=======
def admin_userpermission_change(token, u_id, permission_id):
    pass
>>>>>>> dev
=======
def admin_userpermission_change(token, u_id, permission_id):
    pass
>>>>>>> 4250d04268f97679940622e88326f0d422e16b07

def search(token, query_str):
    return {
        'messages': [{
            'message_id': 1,
            'u_id': 1,
            'message': 'Hello world',
            'time_created': 1582426789,
        }],
    }