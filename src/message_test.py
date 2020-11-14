'''
Message Test
'''
import pytest
from time import sleep
from error import InputError, AccessError
from auth import auth_register
from channel import channel_messages, channel_invite
from channels import channels_create
from message import message_send, message_remove, message_edit, message_pin, message_unpin, message_sendlater, message_react, message_unreact
from message_helper import get_channel, get_message_owner, get_message
from other import clear
from utils import get_current_timestamp


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
        get_channel(10)


def test_get_message_owner():
    '''
    Get invalid owner
    '''
    clear()
    with pytest.raises(InputError):
        get_message_owner(1)


#sendlater


def test_sendlater_invalid_token():
    '''
    Check that an access error is raised when sendlater is given an invalid token
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "validpassword",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com", "validpassword",
                                      "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    time_sent = get_current_timestamp(2)
    with pytest.raises(AccessError):
        message_sendlater(unauthorized_user['token'],
                          new_channel['channel_id'], "message", time_sent)


def test_sendlater_invalid_inputs():
    '''
    Check that errors are raised when sendlater is given invalid inputs
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    time_sent = get_current_timestamp(2)
    time_sent_invalid = get_current_timestamp(-10)
    with pytest.raises(InputError):
        message_sendlater(authorized_user['token'], -1, 'message', time_sent)
    with pytest.raises(InputError):
        message_sendlater(authorized_user['token'], new_channel['channel_id'],
                          'a' * 1001, time_sent)

    with pytest.raises(InputError):
        message_sendlater(authorized_user['token'], new_channel['channel_id'],
                          '', time_sent)
    with pytest.raises(InputError):
        message_sendlater(authorized_user['token'], new_channel['channel_id'],
                          'message', time_sent_invalid)


def test_sendlater_valid_inputs():
    '''
    Check that message is added to channels message after a delay
    '''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    time_sent = get_current_timestamp() + 2
    message_sendlater(authorized_user['token'], new_channel['channel_id'],
                      "message", time_sent)
    assert len(
        channel_messages(authorized_user['token'], new_channel['channel_id'],
                         0)['messages']) == 0
    sleep(2.5)
    assert len(
        channel_messages(authorized_user['token'], new_channel['channel_id'],
                         0)['messages']) == 1


# #react
def test_message_react_normal():
    '''Test that legal user react a message'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_react(authorized_user['token'], message['message_id'], 1)
    message_specific = get_message(message['message_id'])
    assert message_specific['reacts'] == [{
        'react_id': 1,
        'u_ids': [authorized_user['u_id']],
        'is_this_user_reacted': True
    }]


def test_message_already_reacted():
    '''Test that if a user react to a message that has already been reacted'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_react(authorized_user['token'], message['message_id'], 1)
    with pytest.raises(InputError):
        message_react(authorized_user['token'], message['message_id'], 1)


def test_message_invalid_react_id():
    '''Test that if a user try to react a message with an invalid react_id'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    with pytest.raises(InputError):
        message_react(authorized_user['token'], message['message_id'], 0)


def test_message_react_user_not_in_channel():
    '''Test that if a user try to react a message when the user is not in that channel'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com",
                                      "valid_password", "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    with pytest.raises(AccessError):
        message_react(unauthorized_user['token'], message['message_id'], 1)


#unreact
def test_message_unreact_norm():
    '''Test that a legal user unreact on a piece of message'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_react(authorized_user['token'], message['message_id'], 1)
    message_unreact(authorized_user['token'], message['message_id'], 1)
    message_specific = get_message(message['message_id'])
    assert message_specific['reacts'] == [{
        'is_this_user_reacted': False,
        'react_id': 1,
        'u_ids': []
    }]


def test_message_unreact_invalid_react_id():
    '''Test that a legal user unreact a message but with invalid react_id'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_react(authorized_user['token'], message['message_id'], 1)
    with pytest.raises(InputError):
        message_unreact(authorized_user['token'], message['message_id'], 0)


def test_message_unreact_user_not_in_channel():
    ''''Test that if a user try to unreact a message when he is not in that channel'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com",
                                      "valid_password", "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_react(authorized_user['token'], message['message_id'], 1)
    with pytest.raises(AccessError):
        message_unreact(unauthorized_user['token'], message['message_id'], 1)


def test_message_unreact_no_reacts():
    '''Test that if a user try to unreact a message when there is no reacts in message'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    with pytest.raises(InputError):
        message_unreact(authorized_user['token'], message['message_id'], 1)


def test_message_unreact_user_not_react():
    '''Test that if a user try to unreact a message which is not his/her reaction'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com",
                                      "valid_password", "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    channel_invite(authorized_user['token'], new_channel['channel_id'],
                   unauthorized_user['u_id'])
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    with pytest.raises(InputError):
        message_unreact(unauthorized_user['token'], message['message_id'], 1)


# #pin
def test_message_pin_normal():
    '''Test pin on message'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_pin(authorized_user['token'], message['message_id'])
    message_specific = get_message(message['message_id'])
    assert message_specific['is_pinned']


def test_message_pin_invalid_message_id():
    '''Test on invalid message id'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    channels_create(authorized_user['token'], "public_channel", True)
    with pytest.raises(InputError):
        message_pin(authorized_user['token'], -1)


def test_message_pin_not_member():
    '''Test that try to pin a message by a user who ise not a member'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com",
                                      "valid_password", "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    with pytest.raises(AccessError):
        message_pin(unauthorized_user['token'], message['message_id'])


def test_message_already_pinned():
    '''Test that try to pin a message that has already been pinned'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_pin(authorized_user['token'], message['message_id'])
    with pytest.raises(InputError):
        message_pin(authorized_user['token'], message['message_id'])


def test_message_pin_not_owner():
    '''Test that try to pin a  message but not the owner'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com",
                                      "valid_password", "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    channel_invite(authorized_user['token'], new_channel['channel_id'],
                   unauthorized_user['u_id'])
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    with pytest.raises(AccessError):
        message_pin(unauthorized_user['token'], message['message_id'])


# #unpin
def test_message_unpin_normal():
    '''Test unpin on message'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_pin(authorized_user['token'], message['message_id'])
    message_unpin(authorized_user['token'], message['message_id'])
    message_specific = get_message(message['message_id'])
    assert not message_specific['is_pinned']


def test_message_unpin_invalid_message_id():
    '''Test on invalid message id'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    channels_create(authorized_user['token'], "public_channel", True)
    with pytest.raises(InputError):
        message_unpin(authorized_user['token'], -1)


def test_message_unpin_not_member():
    '''Test that try to unpin a message by a user who is not a member'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com",
                                      "valid_password", "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_pin(authorized_user['token'], message['message_id'])
    with pytest.raises(AccessError):
        message_unpin(unauthorized_user['token'], message['message_id'])


def test_message_already_unpinned():
    '''Test that try to unpin a message that has already been unpin'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    with pytest.raises(InputError):
        message_unpin(authorized_user['token'], message['message_id'])


def test_message_unpin_not_owner():
    '''Test that try to unpin a  message but not the owner'''
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    unauthorized_user = auth_register("validEmail2@gmail.com",
                                      "valid_password", "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    channel_invite(authorized_user['token'], new_channel['channel_id'],
                   unauthorized_user['u_id'])
    message = message_send(authorized_user['token'], new_channel['channel_id'],
                           "abcd")
    message_pin(authorized_user['token'], message['message_id'])
    with pytest.raises(AccessError):
        message_unpin(unauthorized_user['token'], message['message_id'])