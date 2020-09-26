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
    # Creating a valid account and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # !!! Not sure how to check for other channels !!!
    # Return empty, since no other channels
    assert channels_list(authorised_user['token']) == {}

def test_channels_list_simple():
    # Creating valid accounts and channels
    # User1
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # User2
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password2", "valid_first2", "valid_last2")
    auth_login("valid_email2@gmail.com", "valid_password2")
    channel_2 = channels_create(authorised_user2['token'], "new_channel2", True)

    # User2 invites User1 to channel_2  
    channel_invite(authorised_user['token'], channel_2, authorised_user['u_id'])
    
    # !!! Not sure how to check for other channels !!!
    assert channels_list(authorised_user['token']) == {}

def test_channels_listall_empty():
    # Creating a valid account and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # Return empty, since no other channels
    assert channels_listall(authorised_user['token']) == {}

def test_channels_listall_simple():
    # Creating valid accounts and channels
    # User 1
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    # User 2
    authorised_user2 = auth_register("validEmail2@gmail.com", "valid_password2", "valid_first2", "valid_last2")
    auth_login("valid_email2@gmail.com", "valid_password2")
    channel_2 = channels_create(authorised_user2['token'], "new_channel2", True)

    # User2 invites User1 to channel_2    
    channel_invite(authorised_user['token'], channel_2, authorised_user['u_id'])
    # !!! Not sure how to check for other channels !!!
    assert channels_listall(authorised_user['token']) == {}

def test_channels_create():
     with pytest.raises(InputError):   
        # Expected to fail, channel name is over 20 characters long (no spaces)
        channels_create(authorised_user['token'], "ThisIsATestForALongChannelName", True)

    with pytest.raises(InputError):   
        # Expected to fail, channel name is over 20 characters long
        channels_create(authorised_user['token'], "The Kanye East experience", False)
