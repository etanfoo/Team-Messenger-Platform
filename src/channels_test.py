from auth import auth_login, auth_register, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
import pytest
from error import InputError, AccessError
from other import clear

def test_channels_list_empty():
    clear() 
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    
    # Return a empty list since no channels were created
    channel_empty = channels_list(authorised_user['token'])
    assert channel_empty['channels'] == []
    clear() 

def test_channels_list_simple():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    #######################################################################################
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    channel_2 = channels_create(new_user2['token'], "new_channel2", True)
    #######################################################################################
    # new_user2 invites authorised_user to channel_2  
    channel_invite(new_user2['token'], channel_2['channel_id'], authorised_user['u_id'])
    
    # Return both channel and channel_2 because of the invitation
    channel_simple = channels_list(authorised_user['token'])
    assert channel_simple['channels'] == [{"channel_id": 0, "name": "new_channel"}, {"channel_id": 1, "name": "new_channel2"}]
    clear() 

def test_channels_list_multiple():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    # Creating mutliple channels.
    channel = channels_create(authorised_user['token'], "new_channel", True)
    channel_2 = channels_create(authorised_user['token'], "new_channel2", True)
    channel_3 = channels_create(authorised_user['token'], "new_channel3", True)
    channel_5 = channels_create(authorised_user['token'], "new_channel5", True)
    
    # Return all channels created
    channel_multiple = channels_list(authorised_user['token'])
    assert channel_multiple['channels'] == [{'channel_id': 0, 'name': 'new_channel'}, {'channel_id': 1, 'name': 'new_channel2'}, {'channel_id': 2, 'name': 'new_channel3'}, {'channel_id': 3, 'name': 'new_channel5'}]
    clear() 

def test_channels_list_uninvited():
    clear()
    uninvited_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    auth_login("validEmail2@gmail.com", "valid_password_2")
    #######################################################################################
    # Creating channels all by new_user2
    channel_20 = channels_create(new_user2['token'], "new_channel20", True)
    channel = channels_create(new_user2['token'], "new_channel", True)
    channel_2 = channels_create(new_user2['token'], "new_channel2", True)
    channel_3 = channels_create(new_user2['token'], "new_channel3", True)

    # Return a empty list since user is not apart of any channels
    channels_uninvited = channels_list(uninvited_user['token'])  
    assert channels_uninvited['channels'] == []
    clear() 

def test_channels_listall_empty():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    
    # Return a empty list since no channels were created
    channel_all_empty = channels_listall(authorised_user['token'])
    assert channel_all_empty['channels']== []
    clear() 

def test_channels_listall_simple():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)
    #######################################################################################
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    auth_login("validEmail2@gmail.com", "valid_password_2")
    channel_2 = channels_create(new_user2['token'], "new_channel2", True)
    #######################################################################################    
    # new_user2 invites authorised_user to channel_2  
    channel_invite(new_user2['token'], channel_2['channel_id'], authorised_user['u_id'])
    
    # Return both channel and channel_2 because of the invitation
    channel_all_simple = channels_listall(authorised_user['token'])
    assert channel_all_simple['channels'] == [{"channel_id": 0, "name": "new_channel"}, {"channel_id": 1, "name": "new_channel2"}]
    clear() 

def test_channels_listall_individual():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "solo_channel", True)
    ####################################################################################### 
    new_user2 = auth_register("validEmail2@gmail.com", "valid_password_2", "Jason", "Henry")
    auth_login("validEmail2@gmail.com", "valid_password_2")
    ####################################################################################### 
    # Creating channels for each user
    channel_invited = channels_create(authorised_user['token'], "invited_channel", True)
    channel_2 = channels_create(new_user2['token'], "solo_channel2", True)
    # authorised_user invites new_user2 to channel_invited
    channel_invite(authorised_user['token'], channel_invited['channel_id'], new_user2['u_id'])
    
    # Return the three channels thave were created because they are all public
    channel_all_individual = channels_listall(authorised_user['token'])
    assert channel_all_individual['channels'] == [{"channel_id": 0, "name": "solo_channel"}, {"channel_id": 1, "name": "invited_channel"}, {"channel_id": 2, "name": "solo_channel2"}]
    clear() 

def test_channels_create_fails():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    ####################################################################################### 
    
    # InputError, channel name is over 20 characters long (no spaces)
    with pytest.raises(InputError):   
        channels_create(authorised_user['token'], "ThisIsATestForALongChannelName", True)
    # InputError, channel name is over 20 characters long
    with pytest.raises(InputError):   
        channels_create(authorised_user['token'], "The Kanye East experience", True)
    clear() 

def test_channels_create_working():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    
    # Testing if the channel_ids increment correctly
    channel = channels_create(authorised_user['token'], "Chicken Nuggets", True)
    assert channel['channel_id'] == 0
    channel_2 = channels_create(authorised_user['token'], "TSM Legends", True)
    assert channel_2['channel_id'] == 1
    clear() 

def test_channels_create_empty():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    
    # InputError, channel name is empty
    with pytest.raises(InputError):   
        channels_create(authorised_user['token'], '', True)
    # InputError, channel name is only spaces
    with pytest.raises(InputError):   
        channels_create(authorised_user['token'], '     ', True)
    clear() 

def test_channels_create_integer():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    
    # Creating channel with purely integers
    channel_num = channels_create(authorised_user['token'], "2020", True)
    assert channel_num['channel_id'] == 0
    clear() 

def test_channels_create_special():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    
    # Creating a channel with special characters.
    channel_special = channels_create(authorised_user['token'], "#*$@*!", True)
    assert channel_special['channel_id'] == 0
    clear() 

def test_channels_create_mix():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")
    #######################################################################################
    
    # Creating channel with mixed numbers and letters. Also special characters
    channel_mix = channels_create(authorised_user['token'], "COVID-19", True)
    assert channel_mix['channel_id'] == 0
    clear() 
