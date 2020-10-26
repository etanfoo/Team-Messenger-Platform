'''
Message Test
'''
import pytest
from error import InputError, AccessError
from auth import auth_register
from channels import channels_create
from message import message_send, message_remove, message_edit
from message_helper import get_channel, get_message_owner, get_message
from other import clear


def test_message_send_size():
    '''
    Message above 1000
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(InputError):
        message_send(authorized_user['token'], new_channel['channel_id'],
                     "x" * 1001)


def test_message_send_invalid_token():
    '''
    Send message with invalid token
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(AccessError):
        message_send(1, new_channel['channel_id'], "hello")


def test_message_send_invalid_channel():
    '''
    Send message with invalid channel
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    with pytest.raises(InputError):
        message_send(authorized_user['token'], 1, "hello")


def test_message_send_authorized():
    '''
    Message send by non authorized user
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    non_authorized_user = auth_register("validEmail2@gmail.com",
                                        "valid_password", "NotAuthorized",
                                        "Person")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(AccessError):
        message_send(non_authorized_user['token'], new_channel['channel_id'],
                     "message")


def test_message_remove_invalid_token():
    '''
    Removing message with invalid token
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message_id = message_send(authorized_user['token'],
                              new_channel['channel_id'],
                              "message")["message_id"]
    with pytest.raises(AccessError):
        message_remove(1, message_id)


def test_message_remove_id_no_exists():
    '''
    Removing message that does not exist
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    with pytest.raises(InputError):
        message_remove(authorized_user['token'], "1")


def test_message_remove_authorized():
    '''
    Remove message by unauthorized user
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    non_authorized_user = auth_register("validEmail2@gmail.com",
                                        "valid_password", "NotAuthorized",
                                        "Person")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    new_channel_2 = channels_create(authorized_user['token'], "public_channel",
                                    True)
    message_id = message_send(authorized_user['token'],
                              new_channel['channel_id'],
                              "message")["message_id"]
    message_id1 = message_send(authorized_user['token'],
                               new_channel_2['channel_id'],
                               "test")["message_id"]
    message_remove(authorized_user['token'], message_id1)
    with pytest.raises(AccessError):
        message_remove(non_authorized_user['token'], message_id)


def test_message_edit_valid_message():
    '''
    Edit message greater than 1001 in length
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    new_channel2 = channels_create(authorized_user['token'], "public_channel",
                                   True)
    message_id = message_send(authorized_user['token'],
                              new_channel['channel_id'],
                              "message")["message_id"]
    message_id2 = message_send(authorized_user['token'],
                               new_channel2['channel_id'],
                               "message")["message_id"]
    message_edit(authorized_user['token'], message_id2, "a" * 10)
    with pytest.raises(InputError):
        message_edit(authorized_user['token'], message_id, "a" * 1001)


def test_message_edit_not_exist():
    '''
    Message edit does not exist
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    channels_create(authorized_user['token'], "public_channel", True)
    with pytest.raises(InputError):
        message_edit(authorized_user['token'], 0, "a")


def test_message_edit_not_authorised():
    '''
    Message edit by non authorized user
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    non_authorized_user = auth_register("validEmail2@gmail.com",
                                        "valid_password", "NotAuthorized",
                                        "Person")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message_id = message_send(authorized_user['token'],
                              new_channel['channel_id'],
                              "message")["message_id"]
    with pytest.raises(AccessError):
        message_edit(non_authorized_user['token'], message_id, "a")


def test_message_edit_none():
    '''
    Message edit none should delete the message
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message_id = message_send(authorized_user['token'],
                              new_channel['channel_id'],
                              "message")["message_id"]
    message_edit(authorized_user['token'], message_id, "")
    with pytest.raises(InputError):
        get_message(message_id)


def test_get_channel():
    '''
    Get the channel
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    auth_register("validEmail2@gmail.com", "valid_password", "NotAuthorized",
                  "Person")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message_id = message_send(authorized_user['token'],
                              new_channel['channel_id'],
                              "message")["message_id"]
    get_channel(message_id)
    with pytest.raises(InputError):
        get_channel(1)


def test_get_message_owner():
    '''
    Get invalid owner
    '''
    clear()
    with pytest.raises(InputError):
        get_message_owner(1)