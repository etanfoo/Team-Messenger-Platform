'''
Tests for other.py. Testing functions users_all, admin_userpermission_change, and search.
'''
import pytest
from auth import auth_login, auth_register, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from message import message_send, message_remove
from other import clear, users_all, admin_userpermission_change, search
from error import InputError, AccessError
from utils import decode_token

'''
users_all function tests
'''

def test_users_all_expected():
    clear()

    # Test if users_all returns expected output when multiple users.
    # Adding users to the data dictionary
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    users_all_expected = users_all(authorised_user['token'])

    assert users_all_expected['users'] == [{"u_id": authorised_user["u_id"], "email": "validEmail@gmail.com", "first_name": 'Philgee', "last_name": "Vlad"}]
    

def test_users_all_multiple():
    clear()

    # Test if users_all returns expected output when multiple users.
    # Adding users to the data dictionary
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Chicken", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Philip", "Denver")
    auth_login("validEmail2@gmail.com", "valid_password")
    authorised_user3 = auth_register("validEmail3@gmail.com", "valid_password", "Zac", "Philip")
    auth_login("validEmail3@gmail.com", "valid_password")

    users_all_expected = users_all(authorised_user['token'])

    assert users_all_expected['users'] == [{"u_id": authorised_user["u_id"], "email": "validEmail@gmail.com", "first_name": 'Chicken', "last_name": "Vlad"},
    {"u_id": authorised_user2["u_id"], "email": "validEmail2@gmail.com", "first_name": 'Philip', "last_name": "Denver"},
    {"u_id": authorised_user3["u_id"], "email": "validEmail3@gmail.com", "first_name": 'Zac', "last_name": "Philip"}] 


    '''
    admin_userpermission_change function tests
    '''


def test_admin_permission_change_new():
    clear()

    # Test if admin+permission_change works as expected when creating a new owner
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    # Making the 2nd user a new admin. auth_user[token] is granting auth_user2[u_id] permission owner
    admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], 1)

    # Check added new owner by calling channel_details
    details = channel_details(authorised_user['token'], channel['channel_id'])

    # Checking both authorised_user and authorised_user2 are owners
    found = 0
    for dictionary in details['owner_members']:
        if authorised_user['u_id'] == dictionary['u_id']:
            found += 1
        elif authorised_user2['u_id'] == dictionary['u_id']:
            found += 1
        elif found == 2:
            break
    # After finding both owners, check only 2 were found
    assert found == 2


def test_admin_permission_change_remove():
    clear()

    # Test if admin+permission_change works as expected when removing an owner
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, removing their owner status
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])
    
    # Making the 2nd user a new admin. auth_user[token] is granting auth_user2[u_id] permission owner
    admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], 1)

    # Check added new owner by calling channel_details
    details = channel_details(authorised_user['token'], channel['channel_id'])

    # Checking both authorised_user and authorised_user2 are owners
    found = 0
    for dictionary in details['owner_members']:
        if authorised_user['u_id'] == dictionary['u_id']:
            found += 1
        elif authorised_user2['u_id'] == dictionary['u_id']:
            found += 1
        elif found == 2:
            break
    # After finding both owners, check only 2 were found
    assert found == 2

    # After confirming there are 2 owners, remove authorised_user2's permissions
    admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], 2)

    # Check added new owner by calling channel_details
    details = channel_details(authorised_user['token'], channel['channel_id'])

    # Checking both authorised_user and authorised_user2 are owners. 0: False, 1: True
    found = 0
    for dictionary in details['owner_members']:
        if authorised_user2['u_id'] == dictionary['u_id']:
            found = 1
    # After finding both owners, check only 2 were found
    assert found == 0

    
def test_admin_permission_change_remove_single_self():
    clear()

    # Test if admin+permission_change works as expected when an owner removes their own permission
    # If owner is the only admin, they cannot remove themself
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # Attempting to remove owner status from themself
    # Raise AccessError as Admin cannot remove their own role
    with pytest.raises(AccessError) as e:
        admin_userpermission_change(authorised_user['token'], authorised_user['u_id'], 2)


def test_admin_permission_change_remove_multiple_self():
    clear()

    # Test if admin+permission_change works as expected when an owner removes their own permission
    # If owner is the only admin, they cannot remove themself
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

     # 2nd User, new admin. Inviting them to the channel
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])
    
    # Making the 2nd user a new admin. auth_user[token] is granting auth_user2[u_id] permission owner
    admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], 1)

    # Attempting to remove owner status from themself
    # Raise AccessError as Admin cannot remove their own role
    with pytest.raises(AccessError) as e:
        admin_userpermission_change(authorised_user2['token'], authorised_user2['u_id'], 2)


def test_admin_permission_change_invalid_self_promotion():
    clear()

    # AccessError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    # AccessError when member attempts to promote self to owner
    with pytest.raises(AccessError) as e:
        admin_userpermission_change(authorised_user2['token'], authorised_user2['u_id'], 2)


def test_admin_permission_change_invalid_other_promotion():
    clear()

    # InputError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin.'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    # InputError when member attempts to promote another user to owner 
    with pytest.raises(AccessError) as e:
        admin_userpermission_change(authorised_user2['token'], authorised_user['u_id'], 2)


def test_admin_permission_change_invalid_user_id():
    clear()

    # InputError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    with pytest.raises(InputError) as e:
        unauthorised_user = auth_register("invalidEmail2@gmail.com", "invalid_password", "In", "Valid")
        admin_userpermission_change(authorised_user2['token'], unauthorised_user['u_id'], 2)


def test_admin_permission_change_empty_user_id():
    clear()

    # InputError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user2['token'], '', 2)


def test_admin_permission_change_invalid_string():
    clear()

    # InputError if user inputs invalid permission type (anything other than member and owner)
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], "string_input")


def test_admin_permission_change_invalid_integer():
    clear()

    # InputError if user inputs invalid permission type (anything other than member and owner)
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], 0)

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], 3)

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], -1)


def test_admin_permission_change_empty_permission():
    clear()

    # InputError if user inputs invalid permission type (anything other than member and owner)
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], None)


'''
search function tests
'''


def test_search_expected():
    clear()

    # Test if user can find pevious messge when there is more than one message
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    message_sent = message_send(authorised_user['token'], channel['channel_id'], 'Old')
    
    search_test = search(authorised_user['token'], 'Old')

    message_access = search_test['messages']
    # Loop through nested dictionary to test if message_id is equal to the message_sent's message id
    found = 0
    for message_data in message_access:
        if message_data["message_id"] == message_sent['message_id']:
            found = 1
    assert found == 1


def test_search_multiple():
    clear()

    # Test if user can find pevious messge when there is more than one message
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    message_sent = message_send(authorised_user['token'], channel['channel_id'], 'Old')
    message_sent2 = message_send(authorised_user['token'], channel['channel_id'], 'Young')

    search_test = search(authorised_user['token'], 'Young')

    message_access = search_test['messages']
    # Loop through nested dictionary to test if message_id is equal to the message_sent's message id
    found = 0
    for message_data in message_access:
        if message_data["message_id"] == message_sent2['message_id']:
            found = 1
    assert found == 1


def test_search_different_user():
    clear()
    
    # Test if user can find pevious messge when other users have messaged
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")
    
    channel = channels_create(authorised_user['token'], "new_channel", True)

    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    auth_login("validEmail2@gmail.com", "valid_password")

    message_sent = message_send(authorised_user['token'], channel['channel_id'], 'Old')
    message_sent2 = message_send(authorised_user['token'], channel['channel_id'], 'Young')

    search_test = search(authorised_user['token'], 'Young')

    message_access = search_test['messages']
    # Loop through nested dictionary to test if message_id is equal to the message_sent's message id
    found = 0
    for message_data in message_access:
        if message_data["message_id"] == message_sent2['message_id']:
            found = 1
    assert found == 1


def test_search_null():
    clear()
    
    # Test if user can find pevious messge
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    # token_decoded = decode_token(authorised_user['token'])

    message_id = message_send(authorised_user['token'], channel['channel_id'], '')["message_id"]
    
    with pytest.raises(InputError):
        message_id = search(authorised_user['token'], None)
