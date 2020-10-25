import pytest
from error import InputError, AccessError
from auth import auth_register, auth_login
from channel import channels_create
from message import message_send, message_remove, message_edit
from message_helper import get_channel, get_message_owner, get_message
from other import clear


#Test message send
#Message above 1000
def test_message_send_size():
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(InputError):
        message_send(authorized_user['token'], new_channel['channel_id'],
                     "x" * 1001)


#Send message with invalid token
def test_message_send_invalid_token():
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(AccessError):
        message_send(1, new_channel['channel_id'], "hello")


#Send message with invalid channel
def test_message_send_invalid_channel():
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    with pytest.raises(InputError):
        message_send(authorized_user['token'], 1, "hello")


#AccessError when: the authorized user has not joined the channel they are trying to post to
def test_message_send_authorized():
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


#Test message remove
def test_message_remove_invalid_token():
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


#InputError when any of:Message (based on ID) no longer exists
def test_message_remove_id_no_exists():
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    with pytest.raises(InputError):
        message_remove(authorized_user['token'], "1")


def test_message_remove_authorized():
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


#AccessError when none of the following are true

#Message with message_id was sent by the authorised user making this request ||
#The authorised user is an owner of this channel or the flockr


#Test message edit
# AccessError when none of the following are true:
# Message with message_id was sent by the authorised user making this request
# The authorised user is an owner of this channel or the flockr
def test_message_edit_valid_message():
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
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(InputError):
        message_edit(authorized_user['token'], 0, "a")


def test_message_edit_not_authorised():
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
    get_channel(message_id)
    with pytest.raises(InputError):
        get_channel(1)


def test_get_message_owner():
    clear()
    with pytest.raises(InputError):
        get_message_owner(1)