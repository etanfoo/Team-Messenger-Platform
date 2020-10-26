'''
Channel Test
'''
import pytest
from auth import auth_login, auth_register, auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create
from error import InputError, AccessError
from other import clear
from message import message_send

# variables to represent invalid id's
INVALID_U_ID = 99999999999
INVALID_CHANNEL_ID = 5555555555


# helper function to register and login
def register_and_login():
    '''
    Helper function to register and login
    '''
    authorised_user = auth_register("validEmail@gmail.com", "valid_password",
                                    "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")

    return authorised_user


def test_channel_invite_normal():
    clear()
    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

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

    clear()


def test_channel_invite_input_error():
    clear()
    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_invite(authorised_user['token'], channel['channel_id'],
                   new_user['u_id'])

    # input error test, when channel_id does not refer to a valid channel
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], INVALID_CHANNEL_ID,
                       new_user['u_id'])

    # input error test, when u_id does not refer to a valid id
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], channel['channel_id'],
                       INVALID_U_ID)

    # input error, when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], "string_input",
                       new_user['u_id'])

    # input error, when u_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_invite(authorised_user['token'], channel['channel_id'],
                       "string_input")

    clear()


def test_channel_invite_access_error():

    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_invite(authorised_user['token'], channel['channel_id'],
                   new_user['u_id'])

    # access error test, when authorised user is not part of channel
    with pytest.raises(AccessError):
        unautharised_user = auth_register("filler@gmail.com", "filler",
                                          "filler", "filler")
        user_invitee = auth_register("invitee@gmail.com", "invitee", "Inv",
                                     "Tee")
        channel_invite(unautharised_user['token'], channel['channel_id'],
                       user_invitee['u_id'])

    clear()


def test_channel_details_normal():
    clear()

    authorised_user = register_and_login()
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

    clear()


def test_channel_details_input_error():
    clear()

    authorised_user = register_and_login()

    # input error test when channel ID is not a valid channel
    with pytest.raises(InputError):
        channel_details(authorised_user['token'], INVALID_CHANNEL_ID)

    # input error test when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_details(authorised_user['token'], "string_input")

    clear()


def test_channel_details_acces_error():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # Access Error when authorised user is not part of channel
    with pytest.raises(AccessError):
        unautharised_user = auth_register("filler@gmail.com", "filler",
                                          "filler", "filler")
        channel_details(unautharised_user['token'], channel['channel_id'])

    clear()


def test_channel_messages_normal():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # sending 100 simple messages, with latest message being 0 and oldest 99
    for i in range(0, 100):
        message_send(authorised_user['token'], channel['channel_id'],
                     f"{99 - i}")

    output = channel_messages(authorised_user['token'], channel['channel_id'],
                              10)

    # checking start and end keys
    assert output['start'] == 10
    assert output['end'] == 60

    index = 0
    # checking message contents
    for j in range(10, 60):
        assert output['messages'][index]['u_id'] == authorised_user['u_id']
        assert output['messages'][index]['message'] == f'{j}'

        index += 1

    clear()


def test_channel_messages_not_enough_messages_remaining():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # sending 100 simple messages, with latest message being 0 and oldest 99
    for i in range(0, 100):
        message_send(authorised_user['token'], channel['channel_id'],
                     f"{99 - i}")

    # testing when start is 70 and < 120 messages in total
    output = channel_messages(authorised_user['token'], channel['channel_id'],
                              70)

    # checking start and end keys
    assert output['start'] == 70
    assert output['end'] == -1

    index = 0
    # checking message contents
    for j in range(70, 100):
        assert output['messages'][index]['u_id'] == authorised_user['u_id']
        assert output['messages'][index]['message'] == f'{j}'

        index += 1

    clear()


def test_channel_messages_input_error():
    # Cant do regular tests as no messages can be sent, according to piazza's instructors answer:

    # "For iteration 1 it's not expected that you test every function to the full extent.
    # Some functions may not be testable at all, and other functions may not be testable
    # until further implementation is done in future iterations."

    clear()

    authorised_user = register_and_login()

    # input error when channel ID not a valid channel
    with pytest.raises(InputError):
        channel_messages(authorised_user['token'], INVALID_CHANNEL_ID, 0)

    # input error when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        channel_messages(authorised_user['token'], "string_input", 0)

    clear()


def test_channel_messages_access_error():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # Access error when user is not a member of channel with channel_id
    with pytest.raises(AccessError):
        new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                                 "Last")
        channel_messages(new_user['token'], channel['channel_id'], 0)

    clear()


def test_channel_leave_regular():

    clear()

    authorised_user = register_and_login()
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
    clear()


def test_channel_leave_input_error():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password",
                                      "One", "Random")
        channel_invite(authorised_user['token'], channel['channel_id'],
                       random_user_1['u_id'])
        channel_leave(random_user_1['token'], INVALID_CHANNEL_ID)

    # input error, when channel_id is not of the same data type as expected (integer)
    with pytest.raises(InputError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password",
                                      "Two", "Random")
        channel_invite(authorised_user['token'], channel['channel_id'],
                       random_user_2['u_id'])
        channel_leave(random_user_2['token'], "string_input")

    clear()


def test_channel_leave_access_error():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # Access error, when user is not a member of channel with channel_id
    with pytest.raises(AccessError):
        random_user_3 = auth_register("random3@gmail.com", "random3_password",
                                      "Three", "Random")
        channel_leave(random_user_3['token'], channel['channel_id'])

    clear()


def test_channel_join_input_error():
    clear()

    #####################################################################################

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password",
                                      "One", "Random")
        channel_join(random_user_1['token'], INVALID_CHANNEL_ID)

    clear()


def test_channel_join_acccess_error():
    clear()
    authorised_user = register_and_login()
    private_channel = channels_create(authorised_user['token'],
                                      "private_new_channel", False)

    # Access error when channel_id refers to a channel that is private (when the authorised user is not an admin)
    with pytest.raises(AccessError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password",
                                      "Two", "Random")
        channel_join(random_user_2['token'], private_channel['channel_id'])

    clear()


def test_channel_join_normal():
    clear()

    authorised_user = register_and_login()
    public_channel = channels_create(authorised_user['token'],
                                     "public_new_channel", True)
    channels_create(authorised_user['token'], "private_new_channel", False)

    #####################################################################################
    # test joining public channel

    # user joins channel
    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_join(new_user['token'], public_channel['channel_id'])

    details = channel_details(authorised_user['token'],
                              public_channel['channel_id'])

    found = False
    for dictionary in details['all_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True
    clear()


def test_channel_addowner_input_error():

    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "public_new_channel",
                              True)

    #####################################################################################

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password",
                                      "One", "Random")
        channel_addowner(authorised_user['token'], INVALID_CHANNEL_ID,
                         random_user_1['u_id'])

    # input error when user with user id u_id is already an owner of the channel
    with pytest.raises(InputError):
        channel_addowner(authorised_user['token'], channel['channel_id'],
                         authorised_user['u_id'])

    clear()


def test_channel_addowner_access_error():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "public_new_channel",
                              True)

    # access error when the authorised user is not an owner of the flockr, or an owner of this channel
    with pytest.raises(AccessError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password",
                                      "Two", "Random")
        channel_addowner(random_user_2['token'], channel['channel_id'],
                         random_user_2['u_id'])

    clear()


def test_channel_addowner_normal():
    clear()

    authorised_user = register_and_login()
    channel = channels_create(authorised_user['token'], "public_new_channel",
                              True)

    #####################################################################################
    # test adding owner to the channel
    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")

    channel_addowner(authorised_user['token'], channel['channel_id'],
                     new_user['u_id'])

    details = channel_details(authorised_user['token'], channel['channel_id'])

    found = False
    for dictionary in details['owner_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == True

    clear()


def test_channel_removeowner_input_error():

    clear()

    authorised_user = register_and_login()
    auth_register("validEmail2@gmail.com", "valid_password", "First", "Last")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # input error when channel ID is not a valid channel
    with pytest.raises(InputError):
        channel_removeowner(authorised_user['token'], INVALID_CHANNEL_ID,
                            authorised_user['u_id'])

    # input error when user with user id u_id is not an owner of the channel
    with pytest.raises(InputError):
        random_user_1 = auth_register("random1@gmail.com", "random1_password",
                                      "One", "Random")
        channel_removeowner(authorised_user['token'], channel['channel_id'],
                            random_user_1['u_id'])

    clear()


def test_channel_removeowner_acces_error():
    clear()

    authorised_user = register_and_login()
    auth_register("validEmail2@gmail.com", "valid_password", "First", "Last")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    # access error when the authorised user is not an owner of the flockr, or an owner of this channel
    with pytest.raises(AccessError):
        random_user_2 = auth_register("random2@gmail.com", "random2_password",
                                      "Two", "Random")
        channel_removeowner(random_user_2['token'], channel['channel_id'],
                            authorised_user['u_id'])

    clear()


def test_channel_removeowner_normal():
    clear()

    authorised_user = register_and_login()
    auth_register("validEmail2@gmail.com", "valid_password", "First", "Last")
    channel = channels_create(authorised_user['token'], "new_channel", True)

    #####################################################################################
    # test adding owner to the channel
    new_user = auth_register("newEmail@gmail.com", "new_password", "New",
                             "Last")
    channel_addowner(authorised_user['token'], channel['channel_id'],
                     new_user['u_id'])
    channel_removeowner(authorised_user['token'], channel['channel_id'],
                        new_user['u_id'])
    details = channel_details(authorised_user['token'], channel['channel_id'])

    found = False
    for dictionary in details['owner_members']:
        if new_user['u_id'] == dictionary['u_id']:
            found = True
            break
    assert found == False

    clear()
