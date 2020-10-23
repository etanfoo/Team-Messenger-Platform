import pytest
from error import InputError, AccessError
from auth import auth_register, auth_login
from channel import channels_create
from message import message_send, message_remove, message_edit
from other import clear


#Test message send
#Message above 1000
def test_message_send_size():
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(InputError):
        message_send(authorized_user['token'], new_channel['channel_id'],
                     "x" * 1001)


#AccessError when: the authorized user has not joined the channel they are trying to post to
def test_message_send_authorized():
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    non_authorized_user = auth_register("validEmail2@gmail.com",
                                        "valid_password", "NotAuthorized",
                                        "Person")
    new_channel = channels_create(authorized_user['token'], "public_channel",
                                  True)
    with pytest.raises(AccessError):
        message_send(non_authorized_user['token'], new_channel['channel_id'],
                     "message")


#Test message remove


#InputError when any of:Message (based on ID) no longer exists
def test_message_remove_id_no_exists():
    clear()
    authorized_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    with py.test.raises(InputError):
        message_remove(authorised_user['token'], "5")


#AccessError when none of the following are true:

#Message with message_id was sent by the authorised user making this request ||
#The authorised user is an owner of this channel or the flockr


#Test message edit
# AccessError when none of the following are true:
# Message with message_id was sent by the authorised user making this request
# The authorised user is an owner of this channel or the flockr
def test_message_edit_owner():
    clear()
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "Philgee", "Vlad")
    not_authorised = auth_register("validEmail1@gmail.com", "valid_password",
                                   "Philgee", "Vlad")
    new_channel = channels_create(authorised_user['token'], "public_channel",
                                  True)
    message_id = message_send(authorised_user['token'],
                              new_channel['channel_id'], "message")
    with pytest.raises(AccessError):
        message_edit(not_authorised['token'], message_id)
