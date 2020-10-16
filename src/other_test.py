from auth import auth_login, auth_register, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
import pytest
from auth import auth_register, auth_login
from message import message_send
from other import clear, users_all, admin_userpermission_change, search
from error import InputError, AccessError
'''
clear function tests
'''
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

    #ASSERT USER LIST

def test_users_all_multiple():
    clear()
    # Test if users_all returns expected output when multiple users.
    # Adding users to the data dictionary
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    authorised_user3 = auth_register("validEmail3@gmail.com", "valid_password", "Riley", "Lewis")
    # Getting list of users
    users_list = users_all(authorised_user['token'])

    #ASSERT USER LIST

    '''
    admin_userpermission_change function tests
    '''

def test_admin_permission_change_new():
    clear()
    # Test if admin+permission_change works as expected when creating a new owner
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
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
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
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
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # Attempting to remove owner status from themself
    admin_userpermission_change(authorised_user['token'], authorised_user['u_id'], 2)

    # Check added new owner by calling channel_details
    details = channel_details(authorised_user['token'], channel['channel_id'])

    # Checking authorised_user is still an owner. 0: False, 1: True
    found = 0
    for dictionary in details['owner_members']:
        if authorised_user['u_id'] == dictionary['u_id']:
            found = 1
    # Check authorised_user is still an owner
    assert found == 1

def test_admin_permission_change_remove_multiple_self():
    clear()
    # Test if admin+permission_change works as expected when an owner removes their own permission
    # If owner is the only admin, they cannot remove themself
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channel = channels_create(authorised_user['token'], "new_channel", True)

     # 2nd User, new admin
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    # Making the 2nd user a new admin. auth_user[token] is granting auth_user2[u_id] permission owner
    admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], 1)

    admin_userpermission_change(authorised_user['token'], authorised_user['u_id'], 2)

    # Check added new owner by calling channel_details
    details = channel_details(authorised_user['token'], channel['channel_id'])

    # Checking authorised_user is still an owner. 0: False, 1: True
    found = 0
    for dictionary in details['owner_members']:
        if authorised_user['u_id'] == dictionary['u_id']:
            found = 1
    # Check if authorised_user was found as an owner
    assert found == 0

# UNSURE ABOUT THIS ONE!!!!!!!!!! HOW TO PROVE U_ID IS INVALID. COME BACK TO THIS
def test_admin_permission_change_invalid_user_id():
    clear()
    # InputError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user2['token'], authorised_user['u_id'], 2)

def test_admin_permission_change_empty_user_id():
    clear()
    # InputError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user2['token'], '', 2)

def test_admin_permission_change_invalid_string():
        clear()
        # InputError if user inputs invalid permission type (anything other than member and owner)
        # Creating channel with admin user
        authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
        channels_create(authorised_user['token'], "new_channel", True)
        # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
        authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

        with pytest.raises(InputError) as e:
            admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], "string_input")

def test_admin_permission_change_invalid_integer():
        clear()
        # InputError if user inputs invalid permission type (anything other than member and owner)
        # Creating channel with admin user
        authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
        channels_create(authorised_user['token'], "new_channel", True)
        # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
        authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

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
        channels_create(authorised_user['token'], "new_channel", True)
        # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
        authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

        with pytest.raises(InputError) as e:
            admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], '')

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

    #MESSAGE SEARCH ASSERT

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

