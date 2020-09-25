from auth import *
from channel import * 
from channels import *
import pytest
from error import InputError, AccessError

def test_invite():
    authorised_user = auth_register("valid_email", "valid_password", "valid_first", "valid_last")
    auth_login("valid_email", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # regular channel invite, u_id should appear in all_members
    new_user = auth_register("new_email", "new_password", "new_first", "new_last")
    channel_invite(authorised_user['token'], channel['channel_id'], new_user['u_id'])
    details = channel_details(authorised_user['token'], channel['channel_id'])
    found = False

    for dictionary in details['all_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True

    # input error test, when channel_id does not refer to a valid channel
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], "invalid_channel", new_user['u_id'])

    # input error test, when u_id does not refer to a valid id
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], channel['channel_id'], "invalid_u_id")
     
    # access error test, when authorised user is not part of channel
    with pytest.raises(AccessError):
        unautharised_user = auth_register("filler", "filler", "filler", "filler")
        channel_invite(unautharised_user['token'], channel['channel_id'], "invalid_u_id")



def test_channel_details():
    pass

def test_channel_messageS():
    pass

def test_channel_leave():
    pass

def test_channel_join():
    pass

def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass

