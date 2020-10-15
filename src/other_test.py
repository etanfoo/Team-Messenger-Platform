import pytest
from error import InputError, AccessError
from auth import auth_register, auth_login
from channel import channels_create
from message import message_send
from global_dic import data
from other import clear, users_all, admin_userpermission_change, search

'''
clear function tests
'''
def test_clear_user():
    clear()
    # Test if clear returns expected output.
    # Adding user to global dictionary
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")

    clear()

    assert data["users"] == []

def test_clear_channel_public():
    clear()
    # Test if clear returns expected output with public channel.
    # Adding user and creating channel.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")

    channels_create(authorised_user['token'], "new_channel", True)

    clear()

    assert data["channels"] == []

def test_clear_channel_private():
    clear()
    # Test if clear returns expected output with private channel.
    # Adding user and creating channel.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")

    channels_create(authorised_user['token'], "new_channel", False)

    clear()

    assert data["channels"] == []

def test_clear_multiple():
    clear()
    # Test if clear returns expected output with both dictionaries containing information.
    # Adding user and creating channel.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password2", "Tara", "Oliver")

    channels_create(authorised_user['token'], "new_channel", True)
    channels_create(authorised_user2['token'], "new_channel", False)

    clear()

    assert data["users"] == []
    assert data["channels"] == []

'''
users_all function tests
'''
def test_users_all_expected():
    clear()
    # Test if users_all returns expected output.
    # Adding users to the data dictionary
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    # Getting list of users
    users_list = users_all(authorised_user['token'])

    assert users_list == {
        'users': [
            {
                'u_id': 1,
                'email': 'validEmail@gmail.com',
                'name_first': 'Philip',
                'name_last': 'Dickens',
                'handle_str': ' ',
            },
        ],
    }

def test_users_all_multiple():
    clear()
    # Test if users_all returns expected output when multiple users.
    # Adding users to the data dictionary
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    authorised_user3 = auth_register("validEmail3@gmail.com", "valid_password", "Riley", "Lewis")
    # Getting list of users
    users_list = users_all(authorised_user['token'])

    assert users_list == {
        'users': [
                {
                    'u_id': 1,
                    'email': 'validEmail@gmail.com',
                    'name_first': 'Philip',
                    'name_last': 'Dickens',
                    'handle_str': ' ',
                },
                {
                    'u_id': 2,
                    'email': 'validEmail2@gmail.com',
                    'name_first': 'Tara',
                    'name_last': 'Simons',
                    'handle_str': ' ',
                },
                {
                    'u_id': 3,
                    'email': 'validEmail3@gmail.com',
                    'name_first': 'Riley',
                    'name_last': 'Lewis',
                    'handle_str': ' ',
                },
            ],
        }

    '''
    admin_userpermission_change function tests
    '''

def test_admin_permission_change_owner():
    clear()
    # Test if admin+permission_change works as expected
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    # Making the 2nd user the new admin. auth_user[token] is granting auth_user2[u_id] permission owner
    admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], authorised_user2['owner'])

    assert data["channels"] == {
        "channels": [
            {
                "name": "channel_name",
                "channel_id": 1,
                "is_public": True,
                "owner_members": [
                    {
                        "u_id": 1,
                    },
                    {
                        "u_id": 2,
                    },
                ],
                "all_members": [
                    {
                        "u_id": 1,
                    },
                    {
                        "u_id": 2,
                    },
                ],
                "messages": [
                    {

                    },
                ],
                # "start": 0,
                # "end": 50,
            },
        ],
    }

def test_admin_permission_change_invalid_user():
    clear()
    # Inputerror if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user['token'], authorised_user2['invaid_u_id'], authorised_user2['owner'])

def test_admin_permission_change_invalid_permission():
        clear()
        # InputError if user inputs invalid permission type (anything other than member and owner)
        # Creating channel with admin user
        authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
        channels_create(authorised_user['token'], "new_channel", True)
        # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
        authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

        with pytest.raises(InputError) as e:
            admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], authorised_user2['queen'])

def test_admin_permission_change__invalid_owner():
    clear()
    # AccessError if user changing permission is not an owner
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

    with pytest.raises(AccessError) as e:
        admin_userpermission_change(authorised_user2['token'], authorised_user2['u_id'], authorised_user2['owner'])

'''
search function tests
'''

def test_search_expected():
    clear()
    # Test if user can find pevious messge
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    message_send(authorised_user['token'], 'new_channel', 'Ready or not, here I come!')

    search_test = search(authorised_user['token'], 'Ready or not, here I come!')

    assert search_test == {
        'messages': [{
            'message_id': 1,
            'u_id': 1,
            'message': 'Ready or not, here I come!',
            'time_created': 'null',
        }],
    }

def test_search_invalid():
    # InputError if message does not exisit
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    message_send(authorised_user['token'], 'new_channel', 'Hello world!')

    with pytest.raises(InputError) as e:
       search_test = search(authorised_user['token'], 'Ready or not, here I come!')

def test_search_partial():
    # InputError if query_str is not the same as the message previously posted.
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    message_send(authorised_user['token'], 'new_channel', 'Hello world!')

    with pytest.raises(InputError) as e:
       search_test = search(authorised_user['token'], 'world!')

