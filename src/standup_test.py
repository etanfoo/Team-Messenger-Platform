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
        standup_start(authorised_user['token'], -1, 50)


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
