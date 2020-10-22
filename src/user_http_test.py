import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from error import InputError
from http_helpers import authorised_user, second_user, register_user, login_user

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
    requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)
    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})

    payload = r.json()
    print(payload)

    assert payload['user']['u_id'] == regular_user['u_id']
    assert payload['user']['email'] == "validEmail@gmail.com"
    assert payload['user']['name_first'] == "Phil"
    assert payload['user']['name_last'] == "Knight"
    assert payload['user']['handle_str'] == "philknight"


# def test_user_profile_input_error_u_id():
#     requests.delete(f"{url}/clear")

#     regular_user = register_user(url, authorised_user)
#     login_user(url, authorised_user)


def test_user_profile_setname_normal():
    requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    requests.put(f"{url}/user/profile/setname", params = {'token' : regular_user['token'], 'name_first' : 'Uncle', 'name_last' : 'Joe'})

    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})
    payload = r.json()

    assert payload['user']['name_first'] == "Uncle"
    assert payload['user']['name_last'] == "Joe"







def test_user_profile_setemail_normal():
    requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    requests.put(f"{url}/user/profile/setemail", params = {'token' : regular_user['token'], 'email' : "NewEmail@gmail.com"})
    
    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})
    payload = r.json()
    
    assert payload['user']['email'] == "NewEmail@gmail.com"






def test_user_profile_sethandle_normal():
    requests.delete(f"{url}/clear")

    regular_user = register_user(url, authorised_user)
    login_user(url, authorised_user)

    requests.put(f"{url}/user/profile/sethandle", params = {'token' : regular_user['token'], 'handle_str' : 'filler'})

    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})

    payload = r.json()
    assert payload['user']['handle_str'] == "filler"

    requests.put(f"{url}/user/profile/sethandle", params = {'token' : regular_user['token'], 'handle_str' : 'Sykkuno'})

    r = requests.get(f"{url}/user/profile", params = {'token' : regular_user['token'], 'u_id' : regular_user['u_id']})
    payload = r.json()

    assert payload['user']['handle_str'] == "Sykkuno"
