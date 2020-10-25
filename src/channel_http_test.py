import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from error import InputError, AccessError
import pytest
from channel import channel_details
from channel_test import INVALID_U_ID, INVALID_CHANNEL_ID
from utils import register_user, login_user, create_channel, invite_channel

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

unauthorised_user = {
    "email": "unauthorised@gmail.com",
    "password": "ILoveSleep",
    "name_first": "Sleepy",
    "name_last": "Joe",
}

'''___________________________________'''
def prepare_user(url, user):
    new_user = register_user(url, user)
    login_user(url, user)
    return new_user

###################
# channel/invite
###################

def test_channel_invite_normal(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)
    # Create user_2
    user_2 = prepare_user(url, second_user)
    # user_1 invites user_2 to channel_1
    requests.post(f"{url}/channel/invite", json={"token": user_1['token'], "channel_id": channel_1['channel_id'], "u_id": user_2['u_id']})
    # grab details of channel 1
    details = requests.get(f"{url}/channel/details", params={"token": user_1['token'], "channel_id": channel_1['channel_id']}).json()
    
    print(details)
    

    # check if you can find all members in all_members
    count = 0
    for members in details['all_members']:
        if members['u_id'] == user_1['u_id'] or members['u_id'] == user_2['u_id']:
            count += 1
        elif count == 2:
            break
    assert count == 2

    # check if owner is in owner_members
    count = 0
    for members in details['owner_members']:
        if members['u_id'] == user_1['u_id'] or members['u_id'] == user_2['u_id']:
            count += 1

    assert count == 1

def test_channel_invite_input_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)
    # Create user_2
    user_2 = prepare_user(url, second_user)

    # input error test, when channel_id does not refer to a valid channel
    payload = requests.post(f"{url}/channel/invite", json={"token": user_1['token'], "channel_id": INVALID_CHANNEL_ID, "user": user_2['u_id']})
    
    assert payload.status_code == 400
    # input error test, when u_id does not refer to a valid id
    payload = requests.post(f"{url}/channel/invite", json={"token": user_1['token'], "channel_id": channel_1['channel_id'], "user": INVALID_U_ID})
    
    assert payload.status_code == 400
    # input error, when channel_id is not of the same data type as expected (integer)
    payload = requests.post(f"{url}/channel/invite", json={"token": user_1['token'], "channel_id": "string_input", "user": user_2['u_id']})
    
    assert payload.status_code == 400
    # input error, when u_id is not of the same data type as expected (integer)
    payload = requests.post(f"{url}/channel/invite", json={"token": user_1['token'], "channel_id": channel_1['channel_id'], "user": "string_input"})
    
    assert payload.status_code == 400
    
def test_channel_invite_access_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)
    # Create user_2
    user_2 = prepare_user(url, second_user)    

    # access error test, when authorised user is not part of channel
    # Create user_3
    user_3 = prepare_user(url, unauthorised_user)
    # user_3 invites user_2 to channel_1
    payload = requests.post(f"{url}/channel/invite", json={"token": user_3['token'], "channel_id": channel_1['channel_id'], "user": user_2['u_id']})
    
    assert payload.status_code == 400

def test_channel_details_normal(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)
    # Create user_2
    user_2 = prepare_user(url, second_user)    

    #####################################################################################
    # regular channel details, should display correct information
    details = requests.get(f"{url}/channel/details", params={"token": user_1['token'], "channel_id": channel_1['channel_id']}).json()
    
    assert details['name'] == "GoodThings"

    # authorised_user should be an owner
    found = False
    for member in details['owner_members']:
        if user_1['u_id'] == member['u_id']:
            found = True
            break
    assert found == True

    # authorised_user should be a member
    found = False
    for member in details['all_members']:
        if user_1['u_id'] == details['u_id']:
            found = True
            break
    assert found == True

    # inviting new user to channel
    invite_channel(url, user_1['token'], channel_1['channel_id'], user_2['u_id'])

    details = requests.get(f"{url}/channel/details", params={"token": user_1['token'], "channel_id": channel_1['channel_id']}).json()
    
    found = False

    # checking new_user found in all members
    for member in details['all_members']:
        if user_2['u_id'] == member['u_id']:
            found = True
            break
    assert found == True

    # checking new_user not found in owner_members
    found = False
    for member in details['owner_members']:
        if user_2['u_id'] == member['u_id']:
            found = True
            break
    assert found == False
    #####################################################################################

def test_channel_details_input_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)

    # input error test when channel ID is not a valid channel
    
    payload = requests.get(f"{url}/channel/details", params = {"token" : user_1['token'], "channel_id" : INVALID_CHANNEL_ID})
    
    assert payload.status_code == 400
    # input error test when channel_id is not of the same data type as expected (integer)
    
    payload = requests.get(f"{url}/channel/details", params = {"token" : user_1['token'], "channel_id" : "string_input"})
    
    assert payload.status_code == 400

def test_channel_details_acces_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    # Access Error when authorised user is not part of channel
    user_3 = prepare_user(url, unauthorised_user)
    payload = requests.get(f"{url}/channel/details", params = {"token" : user_3['token'], "channel_id" : channel_1['channel_id']})
    
    assert payload.status_code == 400


def test_channel_messages_input_error(url):
    # Cant do regular tests as no messages can be sent, according to piazza's instructors answer:

    # "For iteration 1 it's not expected that you test every function to the full extent.
    # Some functions may not be testable at all, and other functions may not be testable
    # until further implementation is done in future iterations."

    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)

    # input error when channel ID not a valid channel
    payload = requests.get(f"{url}/channel/messages", params = {"token" : user_1['token'], "channel_id" : INVALID_CHANNEL_ID, "start" : 0})
    
    assert payload.status_code == 400
    # input error when channel_id is not of the same data type as expected (integer)    
    payload = requests.get(f"{url}/channel/messages", params = {"token" : user_1['token'], "channel_id" : "string_input", "start" : 0})
    
    assert payload.status_code == 400

def test_channel_messages_access_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    # Access error when user is not a member of channel with channel_id
    user_2 = prepare_user(url, unauthorised_user)
    payload = requests.get(f"{url}/channel/messages", params = {"token" : user_2['token'], "channel_id" : channel_1["channel_id"], "start" : 0})
    
    assert payload.status_code == 400

def test_channel_leave_regular(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    #####################################################################################
    # testing regular channel_leave

    # invite new user to channel
    user_2 = prepare_user(url, second_user)
    invite_channel(url, user_1['token'], channel_1['channel_id'], user_2['u_id'])

    # new user leaving, should not be found as a part of all_members
    requests.post(f"{url}/channel/leave", json={user_2['token'], channel_1['channel_id']})
    details = requests.get(f"{url}/channel/details", params={"token": user_1['token'], "channel_id": channel_1['channel_id']}).json()

    found = False
    for members in details['all_members']:
        if user_2['u_id'] == members['u_id']:
            found = True
            break
    assert found == False

    #####################################################################################

def test_channel_leave_input_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    # input error when channel ID is not a valid channel
    user_2 = prepare_user(url, second_user)
    invite_channel(url, user_1['token'], channel_1['channel_id'], user_2['u_id'])

    payload = requests.post(url, json={user_2['token'], INVALID_CHANNEL_ID})
    
    assert payload.status_code == 400
    # input error, when channel_id is not of the same data type as expected (integer)
    user_3 = prepare_user(url, unauthorised_user)
    invite_channel(url, user_1['token'], channel_1['channel_id'], user_3['u_id'])

    payload = requests.post(url, json={user_3['token'], "string_input"})
    
    assert payload.status_code == 400

def test_channel_leave_access_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    # Access error, when user is not a member of channel with channel_id
    user_3 = prepare_user(url, unauthorised_user)
    payload = requests.post(f"{url}/channel/leave", json={user_3['token'], channel_1['channel_id']})
    
    assert payload.status_code == 400

def test_channel_join_input_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)

    #####################################################################################

    # input error when channel ID is not a valid channel
    payload = requests.post(f"{url}/channel/join", json={user_1['token'], INVALID_CHANNEL_ID})
    
    assert payload.status_code == 400

def test_channel_join_acccess_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    private_channel = create_channel(url, user_1['token'], "Private", False)

    # Access error when channel_id refers to a channel that is private (when the authorised user is not an admin)
    user_2 = prepare_user(url, second_user)
    payload = requests.post(f"{url}/channel/join", json={user_2['token'], private_channel['channel_id']})
    
    assert payload.status_code == 400

def test_channel_join_normal(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    public_channel = create_channel(url, user_1['token'], "public_channel", True)

    #####################################################################################
    # test joining public channel

    # user joins channel
    user_2 = prepare_user(url, second_user)
    requests.post(f"{url}/channel/join", json={user_2['token'], public_channel['channel_id']})

    details = requests.get(f"{url}/channel/details", params={"token": user_1['token'], "channel_id": channel_1['channel_id']}).json()

    found = False
    for member in details['all_members']:
        if user_1['u_id'] == member['u_id']:
            found = True
            break
    assert found == True
    
def test_channel_addowner_input_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    #####################################################################################

    # input error when channel ID is not a valid channel
    user_2 = prepare_user(url, second_user)
    payload = requests.post(f"{url}/channel/addowner", json={user_1['token'], INVALID_CHANNEL_ID, user_2['u_id']})
    
    assert payload.status_code == 400

    # input error when user with user id u_id is already an owner of the channel 
    payload = requests.post(f"{url}/channel/addowner", json={user_1['token'], channel_1['channel_id'], user_1['u_id']})
    
    assert payload.status_code == 400

def test_channel_addowner_access_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    # access error when the authorised user is not an owner of the flockr, or an owner of this channel
    user_2 = prepare_user(url, second_user)
    payload = requests.post(f"{url}/channel/addowner", json={user_2['token'], channel_1['channel_id'], user_2['u_id']})
    
    assert payload.status_code == 400

def test_channel_addowner_normal(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    #####################################################################################
    # test adding owner to the channel
    user_2 = prepare_user(url, second_user)

    requests.post(f"{url}/channel/addowner", json={user_1['token'], channel_1['channel_id'], user_2['u_id']})

    details = requests.get(f"{url}/channel/details", params={"token": user_1['token'], "channel_id": channel_1['channel_id']}).json()

    found = False
    for member in details['owner_members']:
        if user_1['u_id'] == member['u_id']:
            found = True
            break
    assert found == True

def test_channel_removeowner_input_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    # input error when channel ID is not a valid channel
    payload = requests.post(f"{url}/channel/removeowner", json={user_1['token'], INVALID_CHANNEL_ID, user_1['u_id']})
    
    assert payload.status_code == 400

    # input error when user with user id u_id is not an owner of the channel
    user_2 = prepare_user(url, second_user)
    payload = requests.post(f"{url}/channel/removeowner", json={user_1['token'], channel_1['channel_id'], user_2['u_id']})
    
    assert payload.status_code == 400

def test_channel_removeowner_acces_error(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    # access error when the authorised user is not an owner of the flockr, or an owner of this channel 
    user_2 = prepare_user(url, second_user)
    payload = requests.post(f"{url}/channel/removeowner", json={user_2['token'], channel_1['channel_id'], user_1['u_id']})
    
    assert payload.status_code == 400

def test_channel_removeowner_normal():
    # Reset/clear data
    requests.delete(f"{url}/clear")
    # Create user_1 and their channel
    user_1 = prepare_user(url, authorised_user)
    channel_1 = create_channel(url, user_1['token'], "GoodThings", True)

    #####################################################################################
    # test adding owner to the channel
    user_2 = prepare_user(url, second_user)

    requests.post(f"{url}/channel/addowner", json={user_1['token'], channel_1['channel_id'], user_2['u_id']})
    requests.post(f"{url}/channel/removeowner", json={user_1['token'], channel_1['channel_id'], user_2['u_id']})
    details = requests.get(f"{url}/channel/details", params={"token": user_1['token'], "channel_id": channel_1['channel_id']}).json()

    found = False
    for member in details['owner_members']:
        if user_1['u_id'] == member['u_id']:
            found = True
            break
    assert found == False

