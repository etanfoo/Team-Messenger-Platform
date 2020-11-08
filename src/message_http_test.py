'''
Message HTTP Test
'''
import re
import signal
from subprocess import Popen, PIPE
from time import sleep
import pytest
from message_helper import get_message
from channel import channel_messages, channel_invite
from utils import (
    register_user, 
    login_user,
    create_channel,
    authorised_user, 
    second_user,
    send_message, 
    send_message_id, 
    remove_message, 
    edit_message,
    get_current_timestamp,
    message_sendlater,
    message_react,
    message_unreact,
    pin_message, 
    unpin_message
)


@pytest.fixture
def url():
    '''
    Fixture to get the url of the server
    '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


# def test_message_send_size(url):
#     '''
#     Message above 1000
#     '''
#     user_1 = register_user(url, authorised_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
#     data = send_message(url, user_1["token"], channel_1["channel_id"],
#                         "x" * 1001)
#     assert data.status_code == 400


# def test_message_send_invalid_token(url):
#     '''
#     Send message with invalid token
#     '''
#     user_1 = register_user(url, authorised_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
#     data = send_message(url, 1, channel_1["channel_id"], "hello")
#     assert data.status_code == 400


# def test_message_send_invalid_channel(url):
#     '''
#     Send message with invalid channel
#     '''
#     user_1 = register_user(url, authorised_user)
#     data = send_message(url, user_1["token"], 1, "hello")
#     assert data.status_code == 400


# def test_message_send_authorised(url):
#     '''
#     Message send by non authorized user
#     '''
#     user_1 = register_user(url, authorised_user)
#     unauthorised_user = register_user(url, second_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
#     data = send_message(url, unauthorised_user["token"],
#                         channel_1["channel_id"], "hello")
#     assert data.status_code == 400


# def test_message_remove_invalid_token(url):
#     '''
#     Removing message with invalid token
#     '''
#     user_1 = register_user(url, authorised_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
#     message = send_message_id(url, user_1["token"], channel_1["channel_id"],
#                               "hello")
#     data = remove_message(url, 1, message["message_id"])
#     assert data.status_code == 400


# def test_message_remove_id_no_exists(url):
#     '''
#     Removing message that does not exist
#     '''
#     user_1 = register_user(url, authorised_user)
#     data = remove_message(url, user_1["token"], 1)
#     assert data.status_code == 400


# def test_message_edit_valid_message(url):
#     '''
#     Remove message by unauthorized user
#     '''
#     user_1 = register_user(url, authorised_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
#     create_channel(url, user_1["token"], "TSM WIN WORLDS", True)
#     message_1 = send_message_id(url, user_1["token"], channel_1["channel_id"],
#                                 "hello")
#     message_2 = send_message_id(url, user_1["token"], channel_1["channel_id"],
#                                 "hello yoo")
#     edit_message(url, user_1["token"], message_2["message_id"], "a" * 10)
#     data = edit_message(url, user_1["token"], message_1["message_id"],
#                         "a" * 1001)
#     assert data.status_code == 400


# def test_message_edit_not_exist(url):
#     '''
#     Message edit does not exist
#     '''
#     user_1 = register_user(url, authorised_user)
#     create_channel(url, user_1["token"], "TSM Legend", True)
#     data = edit_message(url, user_1["token"], 0, "a")
#     assert data.status_code == 400


# def test_message_edit_not_authorised(url):
#     '''
#     Message edit by non authorized user
#     '''
#     user_1 = register_user(url, authorised_user)
#     unauthorised_user = register_user(url, second_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
#     message_1 = send_message_id(url, user_1["token"], channel_1["channel_id"],
#                                 "hello")
#     data = edit_message(url, unauthorised_user["token"],
#                         message_1["message_id"], "a")
#     assert data.status_code == 400


# def test_sendlater_invalid_token(url):
#     '''
#     Check that an access error is raised when sendlater is given an invalid token
#     '''
#     user_1 = register_user(url, authorised_user)
#     unauthorised_user = register_user(url, second_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)    
#     time_sent = get_current_timestamp(2)

#     data = message_sendlater(url, unauthorised_user["token"], channel_1["channel_id"], "message", time_sent)
#     assert data.status_code == 400


# def test_sendlater_invalid_inputs(url):
#     '''
#     Check that errors are raised when sendlater is given invalid inputs
#     '''
#     user_1 = register_user(url, authorised_user)
#     channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)    
    
#     time_sent = get_current_timestamp(2)
#     time_sent_invalid = get_current_timestamp(-10)
#     data = message_sendlater(url, user_1["token"], -1, "message", time_sent)
#     assert data.status_code == 400
#     data = message_sendlater(url, user_1["token"], channel_1["channel_id"], 'a' * 1001, time_sent)
#     assert data.status_code == 400
#     data = message_sendlater(url, user_1["token"], channel_1["channel_id"], "", time_sent)
#     assert data.status_code == 400
#     data = message_sendlater(url, user_1["token"], channel_1["channel_id"], "message", time_sent_invalid)
#     assert data.status_code == 400


def test_sendlater_valid_inputs(url):
    '''
    Check that message is added to channels message after a delay
    '''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)    
    time_sent = get_current_timestamp() + 2
    message_sendlater(url, user_1["token"], channel_1["channel_id"], "message", time_sent)
    print(user_1)
    # assert len(channel_messages(user_1["token"], channel_1['channel_id'], 0)['messages']) == 0
    # sleep(2.5)
    # assert len(channel_messages(user_1["token"], channel_1['channel_id'], 0)['messages']) == 1


def test_message_react_normal(url):
    '''Test that legal user react a message'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    message_react(url, user_1['token'], message['message_id'], 1)
    message_specific = get_message(message['message_id'])
    assert message_specific['reacts'] == [{
        'react_id': 1,
        'u_ids': [authorized_user['u_id']],
        'is_this_user_reacted': True
    }]


def test_message_already_reacted(url):
    '''Test that if a user react to a message that has already been reacted'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    message_react(url, user_1['token'], message['message_id'], 1)
    data = message_react(url, user_1['token'], message['message_id'], 1)
    assert data.status_code == 400


def test_message_invalid_react_id(url):
    '''Test that if a user try to react a message with an invalid react_id'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    data = message_react(url, user_1['token'], message['message_id'], 0)
    assert data.status_code == 400


def test_message_react_user_not_in_channel(url):
    '''Test that if a user try to react a message when the user is not in that channel'''
    user_1 = register_user(url, authorised_user)
    unauthorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    data = message_react(url, unauthorised_user['token'], message['message_id'], 1)
    assert data.status_code == 400

def test_message_unreact_norm(url):
    '''Test that a legal user unreact on a piece of message'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    message_react(url, user_1['token'], message['message_id'], 1)
    message_unreact(url, user_1['token'], message['message_id'], 1)
    message_specific = get_message(message['message_id'])
    assert message_specific['reacts'] == [{
        'is_this_user_reacted': True,
        'react_id': 1,
        'u_ids': []
    }]

def test_message_unreact_invalid_react_id(url):
    '''Test that a legal user unreact a message but with invalid react_id'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    message_react(url, user_1['token'], message['message_id'], 1)
    data = message_unreact(url, user_1['token'], message['message_id'], 0)
    assert data.status_code == 400


def test_message_unreact_user_not_in_channel(url):
    ''''Test that if a user try to unreact a message when he is not in that channel'''
    user_1 = register_user(url, authorised_user)
    unauthorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    data = message_unreact(url, unauthorised_user['token'], message['message_id'], 1)
    assert data.status_code == 400

def test_message_unreact_no_reacts(url):
    '''Test that if a user try to unreact a message when there is no reacts in message'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    data = message_unreact(url, user_1['token'], message['message_id'], 1)
    assert data.status_code == 400


def test_message_unreact_user_not_react(url):
    '''Test that if a user try to unreact a message which is not his/her reaction'''
    user_1 = register_user(url, authorised_user)
    unauthorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    channel_invite(user_1['token'], channel_1['channel_id'], unauthorised_user['u_id'])
    message_react(url, user_1['token'], message['message_id'], 1)
    data = message_unreact(url, unauthorised_user['token'], message['message_id'], 1)
    assert data.status_code == 400


def test_message_pin_normal(url):
    '''Test pin on message'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    pin_message(url, user_1['token'], message['message_id'])
    message_specific = get_message(message['message_id'])
    assert message_specific['is_pinned']


def test_message_pin_invalid_message_id(url):
    '''Test on invalid message id'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True) 
    data =  pin_message(url, user_1['token'], -1)
    assert data.status_code == 400

def test_message_pin_not_member(url):
    '''Test that try to pin a message by a user who ise not a member'''
    user_1 = register_user(url, authorised_user)
    unauthorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    data =  pin_message(url, unauthorised_user['token'],  message["message_id"])
    assert data.status_code == 400

def test_message_already_pinned(url):
    '''Test that try to pin a message that has already been pinned'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    pin_message(url, authorised_user['token'],  message["message_id"])
    data =  pin_message(url, authorised_user['token'],  message["message_id"])
    assert data.status_code == 400

def test_message_pin_not_owner(url):
    '''Test that try to pin a  message but not the owner'''
    user_1 = register_user(url, authorised_user)
    unauthorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    channel_invite(user_1['token'], channel_1['channel_id'], unauthorised_user['u_id'])
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    data =  pin_message(url, unauthorised_user['token'],  message["message_id"])
    assert data.status_code == 400
    

def test_message_unpin_normal(url):
    '''Test unpin on message'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    pin_message(url, user_1['token'], message['message_id'])
    unpin_message(url, user_1['token'], message['message_id'])
    message_specific = get_message(message['message_id'])
    assert not message_specific['is_pinned']


def test_message_unpin_invalid_message_id(url):
    '''Test on invalid message id'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    data =  unpin_message(url, authorised_user['token'],  -1)
    assert data.status_code == 400


def test_message_unpin_not_member(url):
    user_1 = register_user(url, authorised_user)
    unauthorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    pin_message(url, user_1['token'], message['message_id'])
    data =  unpin_message(url, unauthorised_user['token'],  message["message_id"])
    assert data.status_code == 400

def test_message_already_unpinned(url):
    '''Test that try to unpin a message that has already been unpin'''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    data =  unpin_message(url, authorised_user['token'],  message["message_id"])
    assert data.status_code == 400

def test_message_unpin_not_owner(url):
    '''Test that try to unpin a  message but not the owner'''
    user_1 = register_user(url, authorised_user)
    unauthorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    channel_invite(user_1['token'], channel_1['channel_id'], unauthorised_user['u_id'])
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    pin_message(url, authorised_user['token'],  message["message_id"])
    data =  unpin_message(url, unauthorised_user['token'],  message["message_id"])
    assert data.status_code == 400


