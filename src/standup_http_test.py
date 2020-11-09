'''
Standup_HTTP_TEST
'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest
import requests
from utils import (register_user, login_user, create_channel, invite_channel,
                   authorised_user, second_user)


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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


'''
standup_start tests
'''
def test_start_invalid_channel(url):
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    data = requests.post(f"{url}/standup/start",
                         params={
                             "token": user_1['token'],
                             "channel_id": -1,
                             "length": 10,
                         })

    assert data.status_code == 400

def test_start_expected(url):
    '''
    test if standup start returns an exepected output
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    requests.post(f"{url}/standup/start",
                         params={
                             "token": user_1['token'],
                             "channel_id": channel['channel_id'],
                             "length": 10,
                         })


    # activate standup and raise error when called again
    data = requests.post(f"{url}/standup/start",
                         params={
                             "token": user_1['token'],
                             "channel_id": channel['channel_id'],
                             "length": 10,
                         })

    payload = data.json()

    type_check = isinstance(payload, dict)
    assert type_check == True


def test_standup_negative(url):
    '''
    test if standup length is a valid number
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.post(f"{url}/standup/start",
                         params={
                             "token": user_1['token'],
                             "channel_id": channel['channel_id'],
                             "length": -10,
                         })

    assert data.status_code == 400


'''
standup_active
'''
def test_active_invalid_channel(url):
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.get(f"{url}/standup/active",
                         params={
                             "token": user_1['token'],
                             "channel_id": -1,
                         })

    assert data.status_code == 400

def test_active_expected(url):
    '''
    test if standup start returns an exepected output
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.get(f"{url}/standup/active",
                         params={
                             "token": user_1['token'],
                             "channel_id": channel["channel_id"],
                         })

    payload = data.json()

    type_check = isinstance(payload, dict)
    assert type_check == True

'''
standup_send
'''
def test_send_invalid_channel(url):
    '''
    inputerror if standup function recieves an invalid channel_id (-1)
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    data = requests.post(f"{url}/standup/send",
                         params={
                             "token": user_1['token'],
                             "channel_id": -1,
                             "message": "hello hello",
                         })

    assert data.status_code == 400

def test_send_invalid_message(url):
    '''
    inputerror when message sent is over 1000 characters
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.post(f"{url}/standup/send",
                         params={
                             "token": user_1['token'],
                             "channel_id": channel["channel_id"],
                             "message": "x" * 1001,
                         })

    assert data.status_code == 400

def test_send_invalid_user(url):
    '''
    accesserror if user is not a member of the channel is within
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.post(f"{url}/standup/send",
                         params={
                             "token": 1,
                             "channel_id": channel["channel_id"],
                             "message": "hello hello",
                         })

    assert data.status_code == 400

def test_send_expected(url):
    '''
    test if standup start returns an exepected output
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.post(f"{url}/standup/send",
                         params={
                             "token": user_1['token'],
                             "channel_id": channel["channel_id"],
                             "message": "hello hello"                           
                         })

    payload = data.json()

    type_check = isinstance(payload, dict)
    assert type_check == True
