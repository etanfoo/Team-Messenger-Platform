'''
testing standup functions
'''
from time import sleep
import pytest
from standup import standup_start, standup_active, standup_send
from error import AccessError, InputError
from other import clear
from auth import auth_login, auth_register
from channel import channel_invite, channel_messages
from channels import channels_create
from message import message_send
'''
standup_start tests
'''


def test_start_invalid_channel():
    '''
    inputerror if standup function receives an invalid channel_id (-1)
    '''
    clear()

    # creating user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    # checking for inputerror
    with pytest.raises(InputError):
        standup_start(authorised_user['token'], -1, 1)


def test_start_invalid_inactive():
    '''
    inputerror if standup is already active when being called
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # activate standup and raise error when called again
    standup_start(authorised_user['token'], channel['channel_id'], 2)

    with pytest.raises(InputError):
        standup_start(authorised_user['token'], channel['channel_id'], 1)


def test_start_expected():
    '''
    test if standup start returns an expected output
    '''
    clear()
    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)
    standup_result = standup_start(authorised_user['token'],
                                   channel['channel_id'], 1)
    type_check = isinstance(standup_result, dict)
    assert type_check == True

    assert 'time_finish' in standup_result.keys()
    key_check = isinstance(standup_result['time_finish'], int)
    assert key_check == True


def test_standup_empty():
    '''
    test if expected output occurs when no message is sent during standup
    if no message is sent, standup will not be sent as a message
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    standup_start(authorised_user['token'], channel['channel_id'], 1)

    sleep(2)

    check_messages = channel_messages(authorised_user['token'],
                                      channel['channel_id'], 0)
    assert len(check_messages['messages'][channel['channel_id']]['message']) == 0


def test_standup_negative():
    '''
    test if standup length is a valid number
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    # error as standup length is too short
    with pytest.raises(InputError):
        standup_start(authorised_user['token'], channel['channel_id'], -1)


# '''
# standup_active
# '''


def test_active_invalid_channel():
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    clear()

    # creating user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    # checking for inputerror
    with pytest.raises(InputError):
        standup_active(authorised_user['token'], -1)


def test_active_expected():
    '''
    test if standup start returns an exepected output
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    standup_result = standup_active(authorised_user['token'],
                                    channel['channel_id'])

    type_check = isinstance(standup_result, dict)
    assert type_check == True

    assert 'is_active' in standup_result.keys()
    assert 'time_finish' in standup_result.keys()

    is_active_check = isinstance(standup_result['is_active'], bool)
    time_finish_check = isinstance(standup_result['is_active'], int)

    assert is_active_check == True
    assert time_finish_check == True


# '''
# standup_send
# '''


def test_send_invalid_channel():
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    clear()

    # creating user
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
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
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    with pytest.raises(InputError):
        standup_send(authorised_user['token'], channel['channel_id'],
                     "x" * 1001)


def test_send_invalid_inactive():
    '''
    inputerror if standup is not active and standup_send is being called
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)
    standup_start(authorised_user['token'], channel['channel_id'], 1)
    sleep(5)
    # check standup is not active
    active_test = standup_active(authorised_user['token'],
                                 channel['channel_id'])
    assert active_test['is_active'] == False

    # error as standup is inactive
    with pytest.raises(InputError):
        standup_send(authorised_user['token'], channel['channel_id'],
                     'invalid message')


def test_send_invalid_user():
    '''
    accesserror if user is not a member of the channel is within
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    with pytest.raises(AccessError):
        standup_send(1, channel['channel_id'], "invalid user")


def test_send_expected():
    '''
    test if standup start returns an exepected output
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)
    standup_start(authorised_user['token'], channel['channel_id'], 1)
    standup_result = standup_send(authorised_user['token'],
                                  channel['channel_id'], "hello!!")

    type_check = isinstance(standup_result, dict)
    assert type_check == True


def test_send_message_expected():
    '''
    test if standup send has an expected output when adding messages to a channel
    '''
    clear()

    # creating user and channel
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_login("validEmail@gmail.com", "valid_password")

    channel = channels_create(authorised_user['token'], "new_channel", True)

    standup_start(authorised_user['token'], channel['channel_id'], 2)

    standup_send(authorised_user['token'], channel['channel_id'],
                 "testing standup")

    sleep(1)

    check_messages = channel_messages(authorised_user['token'],
                                      channel['channel_id'], 0)

    assert len(check_messages['messages']) == 1