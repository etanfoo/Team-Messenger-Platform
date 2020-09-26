from auth import *
from channel import * 
from channels import *
import pytest
from error import InputError, AccessError

# variables to represent invalid id's
invalid_u_id = 99999999999
invalid_channel_id = 5555555555

def test_invite():
    authorised_user = auth_register("valid_email", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    #####################################################################################
    # regular channel invite, u_id should appear in all_members but not in owner_members
    new_user = auth_register("new_email", "new_password", "new_first", "new_last")
    channel_invite(authorised_user['token'], channel['channel_id'], new_user['u_id'])
    details = channel_details(authorised_user['token'], channel['channel_id'])
    found = False

    # checking found in all members
    for dictionary in details['all_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True

    # checking not found in owner_members
    found = False
    for dictionary in details['owner_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == False
    #####################################################################################

    # input error test, when channel_id does not refer to a valid channel
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], invalid_channel_id, new_user['u_id'])

    # input error test, when u_id does not refer to a valid id
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], channel['channel_id'], invalid_u_id)
     
    # input error, when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], "string_input", new_user['u_id'])

    # input error, when u_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], channel['channel_id'], "string_input")

    # access error test, when authorised user is not part of channel
    with pytest.raises(AccessError):
        unautharised_user = auth_register("filler", "filler", "filler", "filler")
        channel_invite(unautharised_user['token'], channel['channel_id'], invalid_u_id)



def test_channel_details():
    authorised_user = auth_register("valid_email", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    #####################################################################################
    # regular channel details, should display correct information
    details = channel_details(authorised_user['token'], channel['channel_id'])
    assert details['name'] == "new_channel"

    # authorised_user should be an owner
    found = False
    for dictionary in details['owner_members']:
        if authorised_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True

    # authorised_user should be a member
    found = False
    for dictionary in details['all_members']:
        if authorised_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True

    # inviting new user to channel
    new_user = auth_register("new_email", "new_password", "new_first", "new_last")
    channel_invite(authorised_user['token'], channel['channel_id'], new_user['u_id'])
    details = channel_details(authorised_user['token'], channel['channel_id'])
    found = False

    # checking new_user found in all members
    for dictionary in details['all_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True

    # checking new_user not found in owner_members
    found = False
    for dictionary in details['owner_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == False
    #####################################################################################

    # input error test when channel ID is not a valid channel
    with pytest.raises(InputError):
        channel_details(authorised_user['token'], invalid_channel_id)

    # input error test when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_details(authorised_user['token'], "string_input")     

    # Access Error when authorised user is not part of channel
    with pytest.raises(AccessError):
        unautharised_user = auth_register("filler", "filler", "filler", "filler")
        channel_details(unautharised_user['token'], channel['channel_id'])

def test_channel_messageS():
    # not sure how to do yet as no messages can be sent, according to piazza's instructors answer:

    # "For iteration 1 it's not expected that you test every function to the full extent. 
    # Some functions may not be testable at all, and other functions may not be testable 
    # until further implementation is done in future iterations."
    pass

def test_channel_leave():
    pass

def test_channel_join():
    pass

def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass

