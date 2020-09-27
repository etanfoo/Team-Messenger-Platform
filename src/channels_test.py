from auth import *
from channel import * 
from channels import *
from error import InputError
import pytest

'''
Needs work
    - Check if the user is a member of other channels 
'''

def test_channels_list_empty():
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    # Return empty, since no other channels
    channels_list = channels_list(authorised_user['token'])
    assert channels_list['channels'] == {}

def test_channels_list_simple():
    # Creating valid account and channel for authorised_user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # Creating valid account and channel for new_user2
    new_user2 = auth_register("validEmail_2@gmail.com", "valid_password_2", "valid_first_2", "valid_last_2")
    channel_2 = channels_create(new_user2['token'], "new_channel2", True)
    # new_user2 invites authorised_user to channel_2  
    channel_invite(authorised_user['token'], channel_2['channel_id'], authorised_user['u_id'])
    # Obtain the list of channels of authorised_user
    channels_list = channels_list(authorised_user['token'])
    
    # !!! IDK what to do

    assert channels_list['channels'] == {}

def test_channels_listall_empty():
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    # Return empty, since no other channels
    channels_list = channels_list(authorised_user['token'])
    assert channels_list['channels'] == {}

def test_channels_listall_simple():
    # Creating valid account and channel for authorised_user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # Creating valid account and channel for new_user2
    new_user2 = auth_register("validEmail_2@gmail.com", "valid_password_2", "valid_first_2", "valid_last_2")
    channel_2 = channels_create(new_user2['token'], "new_channel2", True)
    # new_user2 invites authorised_user to channel_2     
    channel_invite(authorised_user['token'], channel_2['channel_id'], authorised_user['u_id'])
    # Obtain the list of all channels
    channels_list_all = channels_listall(authorised_user['token'])
    # !!! If we create a global variable for channels 
    whole_list = global_channels_list['channels']
    # The gloabl list should be the same as channels_list
    error = False
    for dictionary in whole_list:
        # List are incorrect
        if channels_list_all['channels'] != dictionary:
            error = True
            break

    assert error = False

def test_channels_create_fails():
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")

    with pytest.raises(InputError):   
        # Expected to fail, channel name is over 20 characters long (no spaces)
        channels_create(authorised_user['token'], "ThisIsATestForALongChannelName", True)

    with pytest.raises(InputError):   
        # Expected to fail, channel name is over 20 characters long
        channels_create(authorised_user['token'], "The Kanye East experience", True)

def test_channels_create_working():
    # Creating a valid account
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "Chicken Nuggets", True)
    assert channel['channel_id'] == 1

    channel_2 = channels_create(authorised_user['token'], "TSM Legends", True)
    assert channel_2['channel_id'] == 2