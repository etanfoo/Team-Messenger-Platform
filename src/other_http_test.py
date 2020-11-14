'''
Other_HTTP_TEST
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
users_all function tests
'''


def test_users_all_expected(url):
    '''
    Test if users_all works as expected when there is a single user
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    data = requests.get(f"{url}/users/all",
                        params={"token": user_1['token']})
    payload = data.json()

    assert payload['users'] == [{
        "u_id": user_1["u_id"],
        "email": "validEmail@gmail.com",
        "name_first": 'Phil',
        "name_last": "Knight",
        'handle_str' : 'philknight',
        'profile_img_url': ''
    }]


def test_users_all_multiple(url):
    '''
    Test if users_all works as expected when there are mutliple users
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create user_1 and their channel
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    user_2 = register_user(url, second_user)
    login_user(url, second_user)

    data = requests.get(f"{url}/users/all",
                        params={"token": user_1['token']})
    payload = data.json()

    assert payload['users'] == [
        {
            "u_id": user_1["u_id"],
            "email": "validEmail@gmail.com",
            "name_first": 'Phil',
            "name_last": "Knight",
            'handle_str' : 'philknight',
            'profile_img_url': ''
        },
        {
            "u_id": user_2["u_id"],
            "email": "validEmail2@gmail.com",
            "name_first": 'Donald',
            "name_last": "Trump",
            'handle_str' : 'donaldtrump',
            'profile_img_url': ''
        },
    ]


'''
admin_userpermission_change function tests
'''


def test_admin_permission_change_invalid_other_deomotion(url):
    '''
    Error when member attempts to remove an owner's permissions
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)
    user_2 = register_user(url, second_user)
    login_user(url, second_user)
    # Creating channel and inviting user 2
    channel = create_channel(url, user_1['token'], "TSM Wins Worlds", True)
    invite_channel(url, user_1['token'], channel['channel_id'], user_2['u_id'])

    data = requests.post(f"{url}/admin/userpermission/change",
                           json={
                               "token": user_2['token'],
                               "u_id": user_1['u_id'],
                               "permission_id": 2
                           })
    assert data.status_code == 400


def test_admin_permission_change_invalid_user_id(url):
    '''
    Error when u_id is empty
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Empty u_id
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.post(f"{url}/admin/userpermission/change",
                           json={
                               "token": user_1['token'],
                               "u_id": '999999',
                               "permission_id": 2
                           })
    assert data.status_code == 400



def test_admin_permission_change_invalid_integer(url):
    '''
    Error if permission_id is not 1 (owner) or 2 (member)
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # string permission
    # Create users 1 and 2.
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    create_channel(url, user_1['token'], "TSM Wins Worlds", True)

    data = requests.post(f"{url}/admin/userpermission/change",
                           json={
                               "token": user_1['token'],
                               "u_id": user_1['u_id'],
                               "permission_id": -1
                           })
    assert data.status_code == 400

    data = requests.post(f"{url}/admin/userpermission/change",
                           json={
                               "token": user_1['token'],
                               "u_id": user_1['u_id'],
                               "permission_id": 0
                           })
    assert data.status_code == 400



'''
search function tests
'''


def test_search_null(url):
    '''
    Error if search query is Null
    '''
    # Reset/clear data
    requests.delete(f"{url}/clear")

    # Create users 1
    user_1 = register_user(url, authorised_user)
    login_user(url, authorised_user)

    data = requests.get(f"{url}/search",
                        params={
                            "token": user_1['token'],
                            "query_str": None
                        })
    assert data.status_code == 400
