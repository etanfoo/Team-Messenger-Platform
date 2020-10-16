import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep

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

def register_user(url, user):
    # Registers a new user
    r = requests.post(f"{url}/auth/register", json=user)
    # r = requests.post(url + "auth/register", json=authorised_user)
    return r.json()

def create_channel(token, name, is_public):
    new_channel = {
        "token": token,
        "name": name,
        "is_public": is_public,
    }
    return new_channel

###################
# Channels_list
###################

def test_list_empty(url):
    '''
    No channels are created
    '''
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")
    new_user = register_user(url, authorised_user)

    r = requests.get(f"{url}/channels/list", params={"token": new_user['token']})
    # r = requests.get(url + "channels/list", params={"token": new_user['token']})
    payload = r.json()
    assert payload['channels'] == []

    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

def test_list_public(url):
    '''
    Public channels are created
    '''
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")
    new_user = register_user(url, authorised_user)
    new_channel = create_channel(new_user['token'], "TSM_0-6", True)
    r = requests.post(url + "channels/create", json=new_channel)
    channel_id = r.json()

    new_user2 = register_user(url, second_user)
    new_channel2 = create_channel(new_user2['token'], "TSM_Wins_Worlds", True)

    r = requests.get(f"{url}/channels/list", params={"token": new_user['token']})
    # r = requests.get(url + "channels/list", params={"token": new_user['token']})
    payload = r.json()
    assert payload['channels'] == [{"channel_id": 0, new_channel["name"]}, {"channel_id": 1, new_channel2["name"]}]


def test_list_private(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_list_mix(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_list_mix_uninvited(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_list_multiple(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_list_uninvited(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

###################
# Channels_listall
###################

def test_listall_empty(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_listall_simple(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_listall_individual(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_listall_private(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_listall_public(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_listall_mix(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_listall_uninvited(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

###################
# Channels_creates
###################

def test_creates_fails(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_creates_success(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_creates_empty(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_creates_integer(url):
    # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_creates_special(url):
        # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_creates_mix(url):
        # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_creates_public(url):
        # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass

def test_creates_private(url):
        # Reset data
    requests.delete(f"{url}/clear")
    # requests.delete(url + "clear")

    new_user = register_user(url)
    pass









