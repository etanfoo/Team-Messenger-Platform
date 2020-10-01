from global_dic import data
<<<<<<< HEAD

=======
>>>>>>> 89d73dc9d445a1c971bdcd0a1614a01252cdd230

def clear_data():
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


def search(token, query_str):
    return {
        'messages': [{
            'message_id': 1,
            'u_id': 1,
            'message': 'Hello world',
            'time_created': 1582426789,
        }],
    }