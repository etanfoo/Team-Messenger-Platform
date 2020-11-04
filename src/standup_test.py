'''
testing standup functions
'''
from time import sleep
import pytest
from standup import standup_start, standup_active, standup_send
from error import AccessError, InputError
from other import clear
from auth import auth_login, auth_register
from channel import channel_invite
from channels import channels_create
from message import message_send

'''
standup_start tests
'''
def test_start_invalid_channel():
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    clear()

    # creating user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    # checking for inputerror
    with pytest.raises(InputError):
        standup_start(authorised_user['token'], -1, 10)

def test_send_invalid_inactive():
    '''
    inputerror if standup is already active when being called
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    # activate standup and raise error when called again
    standup_start(authorised_user['token'], channel['channel_id'], 50)

    with pytest.raises(InputError):
        standup_start(authorised_user['token'], channel['channel_id'], 50)


'''
standup_active
'''
def test_active_invalid_channel():
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    clear()

    # creating user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    # checking for inputerror
    with pytest.raises(InputError):
        standup_active(authorised_user['token'], -1)


'''
standup_send
'''
def test_send_invalid_channel():
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    clear()

    # creating user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    # checking for inputerror
    with pytest.raises(InputError):
        standup_send(authorised_user['token'], -1, "inputerror")

def test_send_invalid_message():
    '''
    inputerror when message sent is over 1000 characters
    '''
    clear()
    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    with pytest.raises(InputError):
        standup_send(authorised_user['token'], channel['channel_id'], "x" * 1001)

def test_send_invalid_inactive():
    '''
    inputerror if standup is not active and standup_send is being called
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    # check standup is not active
    active_test = standup_active(authorised_user['token'], channel['channel_id'])
    assert active_test['is_active'] == 'is_active' 
    # !!!!!!!!!!!!!!!!!!!!!!!! IS THIS BLACKBOX?, UNSURE WHAT TO RETURN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # error as standup is inactive
    with pytest.raises(InputError):
        standup_send(authorised_user['token'], channel['channel_id'], 'invalid message')

def test_send_invalid_user():
    '''
    accesserror if user is not a member of the channel is within
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    with pytest.raises(AccessError):
        standup_send(1, channel['channel_id'], "invalid user")