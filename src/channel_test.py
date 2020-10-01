from auth import auth_login, auth_register, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
import pytest
from error import InputError, AccessError
from other import clear_data

# variables to represent invalid id's
invalid_u_id = 99999999999
invalid_channel_id = 5555555555


def test_channel_invite():
    clear_data()

    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    #####################################################################################
    # regular channel invite, u_id should appear in all_members but not in owner_members
    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_invite(authorised_user['token'], channel['channel_id'],
                   new_user['u_id'])
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
        channel_invite(authorised_user['token'], invalid_channel_id,
                       new_user['u_id'])

    # input error test, when u_id does not refer to a valid id
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], channel['channel_id'],
                       invalid_u_id)

    # input error, when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], "string_input",
                       new_user['u_id'])

    # input error, when u_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], channel['channel_id'],
                       "string_input")

    # access error test, when authorised user is not part of channel
    with pytest.raises(AccessError):
        unautharised_user = auth_register("filler@gmail.com", "filler",
                                          "filler", "filler")
        channel_invite(unautharised_user['token'], channel['channel_id'],
                       invalid_u_id)
    
    clear_data()

def test_channel_details():
    clear_data()

    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")
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
    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_invite(authorised_user['token'], channel['channel_id'],
                   new_user['u_id'])
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
        unautharised_user = auth_register("filler@gmail.com", "filler",
                                          "filler", "filler")
        channel_details(unautharised_user['token'], channel['channel_id'])

    clear_data()

def test_channel_messages():
    # Cant do regular tests as no messages can be sent, according to piazza's instructors answer:

    # "For iteration 1 it's not expected that you test every function to the full extent.
    # Some functions may not be testable at all, and other functions may not be testable
    # until further implementation is done in future iterations."

    clear_data()

    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # input error when channel ID not a valid channel
    with pytest.raises(InputError):
        messages = channel_messages(authorised_user['token'],
                                    invalid_channel_id, 0)

    # input error when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        messages = channel_messages(authorised_user['token'], "string_input",
                                    0)

    # Access error when user is not a emember of channel with channel_id
    with pytest.raises(AccessError):
        new_user = auth_register("newEmail@gmail.com", "new_password",
                                 "New", "Last")
        messages = channel_messages(new_user['token'], channel['channel_id'],
                                    0)

    clear_data()

def test_channel_leave():

    clear_data()

    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    #####################################################################################
    # testing regular channel_leave

    # invite new user to channel
    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_invite(authorised_user['token'], channel['channel_id'],
                   new_user['u_id'])

    # new user leaving, should not be found as a part of all_members
    channel_leave(new_user['token'], channel['channel_id'])
    details = channel_details(authorised_user['token'], channel['channel_id'])

    found = False
    for dictionary in details['all_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == False

    #####################################################################################

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password",
                                      "random1_first", "random1_last")
        channel_invite(authorised_user['token'], channel['channel_id'],
                       random_user_1['u_id'])
        channel_leave(random_user_1['token'], invalid_channel_id)

    # input error, when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password",
                                      "random2_first", "random2_last")
        channel_invite(authorised_user['token'], channel['channel_id'],
                       random_user_2['u_id'])
        channel_leave(random_user_2['token'], "string_input")

    # Access error, when user is not a member of channel with channel_id
    with pytest.raises(AccessError):
        random_user_3 = auth_register("random3@gmail.com", "random3_password",
                                      "random3_first", "random3_last")
        channel_leave(random_user_3['token'], "string_input")

    clear_data()

def test_channel_join():

    clear_data()

    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")
    public_channel = channels_create(authorised_user['token'], "public_new_channel", True)
    private_channel = channels_create(authorised_user['token'], "private_new_channel", False)

    #####################################################################################

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password",
                                      "random1_first", "random1_last")
        channel_join(random_user_1['token'], invalid_channel_id)

    # Access error when channel_id refers to a channel that is private (when the authorised user is not an admin)
    with pytest.raises(AccessError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password", "random2_first", "random2_last")
        channel_join(random_user_2['token'], private_channel['channel_id'])

    #####################################################################################
    # testing can join public channel

    # user joins channel
    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_join(new_user['token'], public_channel)

    details = channel_details(authorised_user['token'],
                              public_channel['channel_id'])

    found = False
    for dictionary in details['all_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True
    clear_data()

def test_channel_addowner():

    clear_data()

    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "public_new_channel", True)

    #####################################################################################

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password",
                                      "random1_first", "random1_last")
        channel_addowner(random_user_1['token'], invalid_channel_id,
                         random_user_1['u_id'])

    # input error when user with user id u_id is already an owner of the channel 
    with pytest.raises(InputError):        
        channel_addowner(authorised_user['token'], channel['channel_id'], authorised_user['u_id'])

    # access error when the authorised user is not an owner of the flockr, or an owner of this channel
    with pytest.raises(AccessError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password", "random2_first", "random2_last")
        channel_addowner(random_user_2['token'], channel['channel_id'], random_user_2['u_id'])

    #####################################################################################
    #
    clear_data()

def test_channel_removeowner():

    clear_data()

    authorised_user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        channel_removeowner(authorised_user['token'], invalid_channel_id,
                            authorised_user['u_id'])

    # input error when user with user id u_id is not an owner of the channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password", "random1_first", "random1_last")
        channel_removeowner(random_user_1['token'], channel['channel_id'], authorised_user['u_id'])

    # access error when the authorised user is not an owner of the flockr, or an owner of this channel -> not done
    with pytest.raises(AccessError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password", "random2_first", "random2_last")
        channel_removeowner(random_user_2['token'], channel['channel_id'], random_user_2['u_id'])

    clear_data()