from auth import auth_login, auth_register, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
import pytest
from error import InputError, AccessError
from other import clear_data

def test_channels_list_empty(): 
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    # Return empty, since no other channels
    channels_list_1 = channels_list(authorised_user['token'])
    assert channels_list_1['channels'] == []
    clear_data()

def test_channels_list_simple():
    # Creating valid account and channel for authorised_user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # Creating valid account and channel for new_user2
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    channel_2 = channels_create(new_user2['token'], "new_channel2", True)
    # new_user2 invites authorised_user to channel_2  
    channel_invite(authorised_user['token'], channel_2['channel_id'], authorised_user['u_id'])
    # Obtain the list of channels of authorised_user
    channels_list_1 = channels_list(authorised_user['token'])

    assert channels_list_1['channels'] == [{"channel_id": 0, "name": "new_channel"}, {"channel_id": 1, "name": "new_channel2"}]
    clear_data()

def test_channels_list_multiple():
    # Test when multiple channels are created. If the program has correct return when user is the creator of more that 1 channel.
    # Creating user's details.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    # Creating mutliple channels.
    channel = channels_create(authorised_user['token'], "new_channel", True)
    channel_2 = channels_create(authorised_user['token'], "new_channel2", True)
    channel_3 = channels_create(authorised_user['token'], "new_channel3", True)
    channel_4 = channels_create(authorised_user['token'], "new_channel4", True)
    channel_5 = channels_create(authorised_user['token'], "new_channel5", True)

    # Obtain the list of channels of authorised_user
    channels_list_1 = channels_list(authorised_user['token'])
    assert channels_list(authorised_user['token']) == {'channels': [{'channel_id': 0, 'name': 'new_channel'}, {'channel_id': 1, 'name': 'new_channel2'}, {'channel_id': 2, 'name': 'new_channel3'}, {'channel_id': 3, 'name': 'new_channel4'}, {'channel_id': 4, 'name': 'new_channel5'}]}
    clear_data()

def test_channels_list_uninvited():
    # If authorised_user is not apart of any channel despite there being many channels.
    uninvited_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    # Creating valid account and channel for new_user2
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    auth_login("validEmail2@gmail.com", "valid_password_2")
    channel_20 = channels_create(new_user2['token'], "new_channel20", True)
    # Creating mutliple channels.
    channel = channels_create(uninvited_user['token'], "new_channel", True)
    channel_2 = channels_create(uninvited_user['token'], "new_channel2", True)
    channel_3 = channels_create(uninvited_user['token'], "new_channel3", True)

    # Obtain the list of channels of authorised_user
    channels_list_1 = channels_list(new_user2['token'])  
    # Return an empty set since user is not apart of any channels.
    assert channels_list_1['channels'] == [{'channel_id': 0, 'name': 'new_channel20'}, {'channel_id': 1, 'name': 'new_channel'}, {'channel_id': 2, 'name': 'new_channel2'}, {'channel_id': 3, 'name': 'new_channel3'}]
    clear_data()

def test_channels_listall_empty():
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    # Return empty, since no other channels
    assert channels_listall(authorised_user['token']) == {'channels': []}
    clear_data()

def test_channels_listall_simple():
    # Creating valid account and channel for authorised_user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # Creating valid account and channel for new_user2
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    channel_2 = channels_create(new_user2['token'], "new_channel2", True)
    # new_user2 invites authorised_user to channel_2     
    channel_invite(authorised_user['token'], channel_2['channel_id'], authorised_user['u_id'])
    # Obtain the list of all channels
    channels_list_all = channels_listall(authorised_user['token'])
    # Ordering may be an issue. Put in alphabetical so its consistent 
    assert channels_list_all['channels'] == [{"channel_id": 0, "name": "new_channel"}, {"channel_id": 1, "name": "new_channel2"}]
    clear_data()

def test_channels_listall_individual():
    # Test to check if all channels are returned despite being completely seperate and cases where users are apart of more than 1
    # Creating valid account and channels for first user.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "solo_channel", True)
    # Channel which the 2nd user is apart of.
    channel_invited = channels_create(authorised_user['token'], "invited_channel", True)
    # Create 2nd user's details.
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    channel_2 = channels_create(new_user2['token'], "solo_channel2", True)
    # Create 2nd channel's invitation
    channel_invite(new_user2['token'], channel_invited['channel_id'], new_user2['u_id'])
    # Get list of all channels
    channels_list_all = channels_listall(authorised_user['token'])

    # Ordering may be an issue. Put in alphabetical so its consistent 
    assert channels_list_all['channels'] == [{"channel_id": 0, "name": "solo_channel"}, {"channel_id": 1, "name": "invited_channel"}, {"channel_id": 2, "name": "solo_channel2"}]
    clear_data()

def test_channels_create_fails():
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    with pytest.raises(InputError):   
        # Expected to fail, channel name is over 20 characters long (no spaces)
        channels_create(authorised_user['token'], "ThisIsATestForALongChannelName", True)

    with pytest.raises(InputError):   
        # Expected to fail, channel name is over 20 characters long
        channels_create(authorised_user['token'], "The Kanye East experience", True)
    clear_data()

def test_channels_create_working():
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "Chicken Nuggets", True)
    assert channel['channel_id'] == 0

    channel_2 = channels_create(authorised_user['token'], "TSM Legends", True)
    assert channel_2['channel_id'] == 1
    clear_data()

def test_channels_create_empty():
    # Test for the creation of a channel with no name. Should fail and ask for a name.
    # Creating a valid user.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    with pytest.raises(InputError) as e:   
        # Expected to fail, channel name has no name
        channels_create(authorised_user['token'], '', True)

    with pytest.raises(InputError) as e:   
        # Expected to fail, channel name is only a space
        channels_create(authorised_user['token'], ' ', True)
    clear_data()

def test_channels_create_integer():
    # Test for the creation of a channel with integers.
    # Creating user.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    # Creating channel with purely numbers
    channel_num = channels_create(authorised_user['token'], "2020", True)
    assert channel_num['channel_id'] == 0
    clear_data()

def test_channels_create_special():
    # Test for the creation of a channel with special characters.
    # Creating user.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    # Creating a channel with special characters.
    channel_special = channels_create(authorised_user['token'], "#*$@*!", True)
    assert channel_special['channel_id'] == 0
    clear_data()

def test_channels_create_mix():
    # Test for the creation of a channel with a mix of special and integer characters.
    # Creating user.
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    # Creating channel with mixed numbers and letters. Also special characters
    assert channels_create(authorised_user['token'], "COVID-19", True) == {'channel_id': 0}
    clear_data()
