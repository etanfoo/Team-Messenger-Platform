import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from error import InputError
import pytest
from utils import (
    register_user, 
    login_user, 
    create_channel, 
    invite_channel, 
    authorised_user, 
    second_user,
    send_message,
    send_message_id,
    remove_message,
    edit_message
)
    

@pytest.fixture
def url():
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
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    r = send_message(url, user_1["token"], channel_1["channel_id"], "x" * 1001)
    assert r.status_code == 400


def test_message_send_invalid_token(url):
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    r = send_message(url, 1, channel_1["channel_id"], "hello")
    assert r.status_code == 400


def test_message_send_invalid_channel(url):
    user_1 = register_user(url, authorised_user)
    r = send_message(url, user_1["token"], 1, "hello")
    assert r.status_code == 400


def test_message_send_authorised(url):
    user_1 = register_user(url, authorised_user)
    non_authorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    r = send_message(url, non_authorised_user["token"], channel_1["channel_id"], "hello")
    assert r.status_code == 400


def test_message_remove_invalid_token(url):
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    r = remove_message(url, 1, message["message_id"])
    assert r.status_code == 400


def test_message_remove_id_no_exists(url):
    user_1 = register_user(url, authorised_user)
    r = remove_message(url, user_1["token"], 1)
    assert r.status_code == 400


def test_message_edit_valid_message(url):
    user_1 = register_user(url, authorised_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    create_channel(url, user_1["token"], "TSM WIN WORLDS", True)
    message_1 = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    message_2 = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello yoo")
    edit_message(url, user_1["token"], message_2["message_id"], "a" * 10)
    r = edit_message(url, user_1["token"], message_1["message_id"], "a" * 1001)
    assert r.status_code == 400


def test_message_edit_not_exist(url):
    user_1 = register_user(url, authorised_user)
    create_channel(url, user_1["token"], "TSM Legend", True)
    r = edit_message(url, user_1["token"], 0, "a")
    assert r.status_code == 400


def test_message_edit_not_authorised(url):
    user_1 = register_user(url, authorised_user)
    non_authorised_user = register_user(url, second_user)
    channel_1 = create_channel(url, user_1["token"], "TSM Legend", True)
    message_1 = send_message_id(url, user_1["token"], channel_1["channel_id"], "hello")
    r = edit_message(url, non_authorised_user["token"], message_1["message_id"], "a")
    assert r.status_code == 400


