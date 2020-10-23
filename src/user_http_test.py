import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from error import InputError
from utils import authorised_user, second_user, register_user, login_user


INVALID_U_ID = 99999999999


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

def test_user_profile_normal(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    print(regular_user)
    login_user(url, authorised_user)
    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})
    print(r)
    payload = r.json()
    print(payload)

    assert payload['user']['u_id'] == regular_user['u_id']
    assert payload['user']['email'] == "validEmail@gmail.com"
    assert payload['user']['name_first'] == "Phil"
    assert payload['user']['name_last'] == "Knight"
    assert payload['user']['handle_str'] == "philknight"


def test_user_profile_input_error_u_id(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : INVALID_U_ID})
    
    assert r.status_code == 400


def test_user_profile_setname_normal(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    requests.put(f"{url}/user/profile/setname", json = {'token' : regular_user['token'], 'name_first' : 'Uncle', 'name_last' : 'Joe'})

    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})
    payload = r.json()

    print(payload)
    assert payload['user']['name_first'] == "Uncle"
    assert payload['user']['name_last'] == "Joe"


def test_user_profile_setname_input_error_name_first_long(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/setname", json = {'token' : regular_user['token'], 'name_first' : 'Uncle' * 20, 'name_last' : 'Joe'})

    assert r.status_code == 400

def test_user_profile_setname_input_error_name_first_short(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/setname", json = {'token' : regular_user['token'], 'name_first' : '', 'name_last' : 'Joe'})

    assert r.status_code == 400


def test_user_profile_setname_input_error_name_last_long(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/setname", json = {'token' : regular_user['token'], 'name_first' : 'Uncle', 'name_last' : 'Joe' * 20})

    assert r.status_code == 400

def test_user_profile_setname_input_error_name_last_short(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/setname", json = {'token' : regular_user['token'], 'name_first' : 'Uncle', 'name_last' : ''})

    assert r.status_code == 400


def test_user_profile_setemail_normal(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    requests.put(f"{url}/user/profile/setemail", json = {'token' : regular_user['token'], 'email' : "NewEmail@gmail.com"})
    
    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})
    payload = r.json()
    
    assert payload['user']['email'] == "NewEmail@gmail.com"

def test_user_profile_setemail_input_error_invalid_email(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/setemail", json = {'token' : regular_user['token'], 'email' : "this_is_not_valid@gmail.com"})
    
    assert r.status_code == 400


def test_user_profile_setemail_input_error_emaily_already_used(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    new_details = {
        "email": "NewEmail@gmail.com",
        "password": "valid_password",
        "name_first": "Woopdidi",
        "name_last": "Scoop",
    }

    register_user(url, new_details)
    login_user(url, new_details)

    r = requests.put(f"{url}/user/profile/setemail", json = {'token' : regular_user['token'], 'email' : "NewEmail@gmail.com"})
    
    assert r.status_code == 400




def test_user_profile_sethandle_normal(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    requests.put(f"{url}/user/profile/sethandle", json = {'token' : regular_user['token'], 'handle_str' : 'filler'})

    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})

    payload = r.json()
    assert payload['user']['handle_str'] == "filler"

    requests.put(f"{url}/user/profile/sethandle", json = {'token' : regular_user['token'], 'handle_str' : 'Sykkuno'})

    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})
    payload = r.json()

    assert payload['user']['handle_str'] == "Sykkuno"


def test_user_profile_sethandle_input_error_too_long(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/sethandle", json = {'token' : regular_user['token'], 'handle_str' : 'long' * 20})

    assert r.status_code == 400

def test_user_profile_sethandle_input_error_too_short(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/sethandle", json = {'token' : regular_user['token'], 'handle_str' : 'DQ'})

    assert r.status_code == 400

def test_user_profile_sethandle_input_error_already_used(url):
    # requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.put(f"{url}/user/profile/sethandle", json = {'token' : regular_user['token'], 'handle_str' : 'IYKYK'})


    new_details = {
        "email": "NewEmail@gmail.com",
        "password": "valid_password",
        "name_first": "Woopdidi",
        "name_last": "Scoop",
    }

    new_user = register_user(url, new_details)
    login_user(url, new_details)

    r = requests.put(f"{url}/user/profile/sethandle", json = {'token' : new_user['token'], 'handle_str' : 'IYKYK'})

    assert r.status_code == 400