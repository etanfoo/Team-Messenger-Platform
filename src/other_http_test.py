import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from error import InputError
from utils import register_user, login_user, create_channel, invite_channel, authorised_user, second_user
from channel import channel_details


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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

'''
users_all http function tests
other/users_all
'''

def test_users_all_expected(url):
    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.get(f"{url}/other/users/all", params={"token": user_1['token']})
    payload = r.json()

    assert payload['users'] == [
        {"u_id": user_1["u_id"], 
        "email": "validEmail@gmail.com", 
        "first_name": 'Phil', 
        "last_name": "Knight"}
    ]


    '''
    admin_userpermission_change function tests
    other/admin_userpermission_change
    '''


def test_admin_permission_change_new(url):
    # Create users 1, and 2 
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    # Creating channel and inviting user 2 to it
    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    invite_channel(url, user_1['token'], channel['channel_id'], user_2['u_id'])

    details = channel_details(user_2['token'], channel['channel_id'])


    r = requests.post(f"{url}/other/admin/userpermission/change", params={"token": user_1['token'], "u_id": user_2['u_id'], "permission_id": 1})
    payload = r.json()

    # Checking both authorised_user and authorised_user2 are owners
    found = 0
    for dictionary in details['owner_members']:
        if user_1['u_id'] == dictionary['u_id']:
            found += 1
        elif user_2['u_id'] == dictionary['u_id']:
            found += 1
        elif found == 2:
            break
    # After finding both owners, check only 2 were found
    assert found == 2


def test_admin_permission_change_remove(url):
    # Create users 1, and 2 
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    # Creating channel and inviting user 2 to it
    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    invite_channel(url, user_1['token'], channel['channel_id'], user_2['u_id'])

    details = channel_details(user_2['token'], channel['channel_id'])


    r = requests.post(f"{url}/other/admin/userpermission/change", params={"token": user_1['token'], "u_id": user_2['u_id'], "permission_id": 1})
    payload = r.json()

    # Checking both authorised_user and authorised_user2 are owners
    found = 0
    for dictionary in details['owner_members']:
        if user_1['u_id'] == dictionary['u_id']:
            found += 1
        elif user_2['u_id'] == dictionary['u_id']:
            found += 1
        elif found == 2:
            break
    # After finding both owners, check only 2 were found
    assert found == 2

    r = requests.delete(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": user_2['u_id'], "permission_id": 2})
    payload = r.json()

    # Check added new owner by calling channel_details
    details = channel_details(authorised_user['token'], channel['channel_id'])

    # Checking both authorised_user and authorised_user2 are owners. 0: False, 1: True
    found = 0
    for dictionary in details['owner_members']:
        if user_2['u_id'] == dictionary['u_id']:
            found = 1
    # After finding both owners, check only 2 were found
    assert found == 0

    
def test_admin_permission_change_remove_single_self(url):
    # Create users 1 
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    # Creating channel
    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    r = requests.post(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": user_1['u_id'], "permission_id": 2})
    payload = r.json()

    assert payload["channels"]["owner_members"] != []


def test_admin_permission_change_invalid_self_promotion(url):
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    # Creating channel and inviting user 2
    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    invite_channel(url, user_1['token'], channel['channel_id'], user_2['u_id'])

    r = requests.post(f"{url}/other/admin/userpermission/remove", params={"token": user_2['token'], "u_id": user_2['u_id'], "permission_id": 1})
    payload = r.json()

    assert payload["channels"]["owner_members"] == [{'u_id': user_1["u_id"]}]


def test_admin_permission_change_invalid_other_deomotion(url):
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    # Creating channel and inviting user 2
    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    invite_channel(url, user_1['token'], channel['channel_id'], user_2['u_id'])

    r = requests.delete(f"{url}/other/admin/userpermission/remove", params={"token": user_2['token'], "u_id": user_1['u_id'], "permission_id": 2})
    payload = r.json()

    assert payload["channels"]["owner_members"] == [{'u_id': user_1["u_id"]}]


def test_admin_permission_change_empty_user_id(url):
    # Empty u_id
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    
    r = requests.delete(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": '', "permission_id": 2})
    assert r.status_cose == 400


def test_admin_permission_change_invalid_string(url):
    # string permission
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    
    r = requests.post(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": user_1['u_id'], "permission_id": 'string_input'})
    assert r.status_cose == 400

def test_admin_permission_change_invalid_integer(url):
    # string permission
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    
    r = requests.post(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": user_1['u_id'], "permission_id": -1})
    assert r.status_cose == 400

    r = requests.post(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": user_1['u_id'], "permission_id": 0})
    assert r.status_cose == 400

    r = requests.post(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": user_1['u_id'], "permission_id": 1})
    assert r.status_cose == 400


def test_admin_permission_change_empty_permission(url):
    # string permission
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    
    r = requests.post(f"{url}/other/admin/userpermission/remove", params={"token": user_1['token'], "u_id": user_1['u_id'], "permission_id": ''})
    assert r.status_cose == 400


'''
search function tests
'''


def test_search_expected(url):
    # Create users 1
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    message_sent = message_send(authorised_user['token'], channel['channel_id'], 'Hello')
    
    search_test = search(authorised_user['token'], 'Hello')

    r = requests.post(f"{url}/other/search", params={"token": user_1['token'], "query_str": 'Hello'})
    payload = r.json()

    assert payload['channels']['messages'] == [
        {"u_id": user_1["u_id"], 
        "message_id": search_test['message_id'], 
        "message": "Hello", 
        "time_created": search_test['time_created']}
    ]


def test_search_multiple(url):
    clear()

    # Test if user can find pevious messge when there is more than one message
    # Creating user, channel, and posting message
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    message_sent = message_send(authorised_user['token'], channel['channel_id'], 'Old')
    message_sent2 = message_send(authorised_user['token'], channel['channel_id'], 'Young')

    search_test = search(authorised_user['token'], 'Young')


    r = requests.post(f"{url}/other/search", params={"token": user_1['token'], "query_str": 'Young'})
    payload = r.json()

    assert payload['channels']['messages'] == [
        {"u_id": user_1["u_id"], 
        "message_id": search_test['message_id'], 
        "message": "Hello", 
        "time_created": search_test['time_created']}
    ]


def test_search_different_user(url):
    # Test if user can find pevious messge when there is more than one message
    # Creating user, channel, and posting message
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    user_2 = register_user(url, second_user)
    login_user(url, second_user)

    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    invite_channel(url, user_1['token'], channel['channel_id'], user_2['u_id'])

    message_sent = message_send(authorised_user['token'], channel['channel_id'], 'Old')
    message_sent2 = message_send(second_user['token'], channel['channel_id'], 'Young')

    search_test = search(authorised_user['token'], 'Young')


    r = requests.post(f"{url}/other/search", params={"token": user_2['token'], "query_str": 'Old'})
    payload = r.json()

    assert payload['channels']['messages'] == [
        {"u_id": user_1["u_id"], 
        "message_id": search_test['message_id'], 
        "message": "Hello", 
        "time_created": search_test['time_created']}
    ]


def test_search_null(url):
    # Create users 1
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    r = requests.post(f"{url}/other/search", params={"token": user_1['token'], "query_str": ''})
    assert r.status_cose == 400
   

'''
def test_echo(url):

    A simple test to check echo

    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}
'''