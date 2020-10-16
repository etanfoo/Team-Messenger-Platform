from auth import auth_login, auth_register, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
import pytest
from auth import auth_register, auth_login
from message import message_send, message_remove, message_edit
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
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, removing their owner status
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

     # 2nd User, new admin. Inviting them to the channel
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])
    
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

def test_admin_permission_change_invalid_self_promotion():
    clear()
    # AccessError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    # AccessError when member attempts to promote another self to owner
    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user2['token'], authorised_user2['u_id'], 2)

def test_admin_permission_change_invalid_other_promotion():
    clear()
    # AccessError if user's u_id refers to an invalid user
    # Creating channel with admin user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    # AccessError when member attempts to promote another user to owner 
    with pytest.raises(InputError) as e:
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
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
    channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

    with pytest.raises(InputError) as e:
        admin_userpermission_change(authorised_user2['token'], '', 2)

def test_admin_permission_change_invalid_string():
        clear()
        # InputError if user inputs invalid permission type (anything other than member and owner)
        # Creating channel with admin user
        authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
        channel = channels_create(authorised_user['token'], "new_channel", True)
        # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
        authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
        channel_invite(authorised_user['token'], channel['channel_id'], authorised_user2['u_id'])

        with pytest.raises(InputError) as e:
            admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], "string_input")

def test_admin_permission_change_invalid_integer():
        clear()
        # InputError if user inputs invalid permission type (anything other than member and owner)
        # Creating channel with admin user
        authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
        channel = channels_create(authorised_user['token'], "new_channel", True)
        # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
        authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")
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
        channel = channels_create(authorised_user['token'], "new_channel", True)
        # 2nd User, new admin. 2nd user's u_id is 'u_id: 2'
        authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")

        with pytest.raises(InputError) as e:
            admin_userpermission_change(authorised_user['token'], authorised_user2['u_id'], None)

'''
search function tests
Until implementation is complete, message_sent will return a message_id of 1.
Thus, tests not check type/access errors will pass.
'''
def test_search_expected():
    clear()
    # Test if user can find pevious messge
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)
    message_sent = message_send(authorised_user['token'], 'new_channel', 'Hello world')

    search_test = search(authorised_user['token'], 'Hello world')

    message_access = search_test['messages']
    # Loop through nested dictionary to test if message_id is equal to the message_sent's message id
    for message_data in message_access:
        assert message_data["message_id"] == message_sent['message_id']

def test_search_multiple():
    clear()
    # Test if user can find pevious messge when there is more than one message
    # Creating user, channel, and posting message
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philip", "Dickens")
    channels_create(authorised_user['token'], "new_channel", True)

    message_sent = message_send(authorised_user['token'], 'new_channel', 'Old')
    message_sent2 = message_send(authorised_user['token'], 'new_channel', 'Young')

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
    channels_create(authorised_user['token'], "new_channel", True)

    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password", "Tara", "Simons")


    message_sent = message_send(authorised_user['token'], 'new_channel', 'Old')
    message_sent2 = message_send(authorised_user['token'], 'new_channel', 'Young')

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
    channels_create(authorised_user['token'], "new_channel", True)

    message_sent = message_send(authorised_user['token'], 'new_channel', 'Old')
    
    with pytest.raises(InputError):
        search_test = search(authorised_user['token'], None)
