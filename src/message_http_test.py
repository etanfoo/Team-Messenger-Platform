'''
Message HTTP Test
'''
import re
import signal
from subprocess import Popen, PIPE
from time import sleep
import pytest
from utils import (register_user, create_channel, authorised_user, second_user,
                   send_message, send_message_id, remove_message, edit_message)


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


def test_message_send_size(url):
    '''
    Message above 1000
    '''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    data = send_message(url, user_1["token"], channel_1["channel_id"],
                        "x" * 1001)
    assert data.status_code == 400


def test_message_send_invalid_token(url):
    '''
    Send message with invalid token
    '''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    data = send_message(url, 1, channel_1["channel_id"], "hello")
    assert data.status_code == 400


def test_message_send_invalid_channel(url):
    '''
    Send message with invalid channel
    '''
    user_1 = register_user(url, authorised_user)
    data = send_message(url, user_1["token"], 1, "hello")
    assert data.status_code == 400


def test_message_send_authorised(url):
    '''
    Message send by non authorized user
    '''
    user_1 = register_user(url, authorised_user)
    non_authorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    data = send_message(url, non_authorised_user["token"],
                        channel_1["channel_id"], "hello")
    assert data.status_code == 400


def test_message_remove_invalid_token(url):
    '''
    Removing message with invalid token
    '''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message = send_message_id(url, user_1["token"], channel_1["channel_id"],
                              "hello")
    data = remove_message(url, 1, message["message_id"])
    assert data.status_code == 400


def test_message_remove_id_no_exists(url):
    '''
    Removing message that does not exist
    '''
    user_1 = register_user(url, authorised_user)
    data = remove_message(url, user_1["token"], 1)
    assert data.status_code == 400


def test_message_edit_valid_message(url):
    '''
    Remove message by unauthorized user
    '''
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    create_channel(url, user_1["token"], "TSM WIN WORLDS", True)
    message_1 = send_message_id(url, user_1["token"], channel_1["channel_id"],
                                "hello")
    message_2 = send_message_id(url, user_1["token"], channel_1["channel_id"],
                                "hello yoo")
    edit_message(url, user_1["token"], message_2["message_id"], "a" * 10)
    data = edit_message(url, user_1["token"], message_1["message_id"],
                        "a" * 1001)
    assert data.status_code == 400


def test_message_edit_not_exist(url):
    '''
    Message edit does not exist
    '''
    user_1 = register_user(url, authorised_user)
    create_channel(url, user_1["token"], "TSM Legend", True)
    data = edit_message(url, user_1["token"], 0, "a")
    assert data.status_code == 400


def test_message_edit_not_authorised(url):
    '''
    Message edit by non authorized user
    '''
    user_1 = register_user(url, authorised_user)
    non_authorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message_1 = send_message_id(url, user_1["token"], channel_1["channel_id"],
                                "hello")
    data = edit_message(url, non_authorised_user["token"],
                        message_1["message_id"], "a")
    assert data.status_code == 400
