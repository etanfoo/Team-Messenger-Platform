import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from error import InputError
import pytest
from channel import channel_details
from channel_test import invalid_u_id, invalid_channel_id


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

###################
# Global variables
###################

authorised_user = {
    "email": "validEmail@gmail.com",
    "password": "valid_password",
    "name_first": "Phil",
    "name_last": "Knight",
}

second_user = {
    "email": "validEmail2@gmail.com",
    "password": "valid_password2",
    "name_first": "Donald",
    "name_last": "Trump",
}

###################
# Helper functions
###################

def register_user(url, user):
    # Registers a new user
    r = requests.post(f"{url}/auth/register", json = user)
    return r.json()

def login_user(url, user):
    # Registers a new user
    requests.post(f"{url}/auth/login", json = {
        "email": user['email'], 
        "password": user['password']
    })

def create_channel(url, token, name, is_public):
    # Creates a new channel
    new_channel = {
        "token": token,
        "name": name,
        "is_public": is_public,
    }
    r = requests.post(f"{url}/channels/create", json = new_channel)
    payload = r.json()
    payload["name"] = new_channel["name"]
    return payload

def invite_channel(url, token, channel_id, u_id):
    # Invites a user to a channel
    invite = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id,
    }
    r = requests.post(f"{url}/channel/invite", json = invite)
    return r.json()

###################
# channel/invite
###################

def test_channel_invite_normal(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)
    # Create user_2 and their channel
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    # user_1 invites user_2 to channel_1
    requests.post(f"{url}/channel/invite", data = {"token": user_1['token'], "channel_id": channel_1['channel_id'], "user": user_2['u_id']})
    # grab details of channel 1
    details = channel_details(user_1['token'], channel_1['channel_id'])

    # check if you can find all members in all_members
    count = 0
    for members in details[2]:
        if members['u_id'] == user_1['u_id'] or members['u_id'] == user_2['u_id']:
            count += 1
        elif count == 2:
            break
    assert count == 2

    # check if owner is in owner_members
    count = 0
    for members in details[1]:
        if members['u_id'] == user_1['u_id'] or members['u_id'] == user_2['u_id']:
            count += 1

    assert count == 1


def test_channel_invite_input_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)
    # Create user_2 and their channel
    user_2 = register_user(url, second_user)
    login_user(url, second_user)

    # input error test, when channel_id does not refer to a valid channel
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/invite", data = {"token": user_1['token'], "channel_id": invalid_channel_id, "user": user_2['u_id']})
    # input error test, when u_id does not refer to a valid id
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/invite", data = {"token": user_1['token'], "channel_id": channel_1['channel_id'], "user": invalid_u_id)
    # input error, when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/invite", data = {"token": user_1['token'], "channel_id": "string_input", "user": user_2['u_id']})
    # input error, when u_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/invite", data = {"token": user_1['token'], "channel_id": channel_1['channel_id'], "user": "string_input")
    
