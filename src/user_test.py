import pytest
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_login, auth_register, auth_register
from other import clear
from error import InputError

INVALID_U_ID = 99999999999

# function to register a user and log them in
def register_user():
    user = auth_register("validEmail@gmail.com", "valid_password", "First", "Last")
    auth_login("validEmail@gmail.com", "valid_password")

    return user


def test_user_profile_normal():
    clear()

    regular_user = register_user()
    
    profile = user_profile(regular_user['token'], regular_user['u_id'])

    assert profile['user']['u_id'] == regular_user['u_id']
    assert profile['user']['email'] == "validEmail@gmail.com"
    assert profile['user']['name_first'] == "First"
    assert profile['user']['name_last'] == "Last"
    assert profile['user']['handle_str'] == "firstlast"

    clear()

def test_user_profile_input_error_u_id():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile(regular_user['token'], INVALID_U_ID)

    clear()


def test_user_profile_setname_normal():
    clear()

    regular_user = register_user()

    user_profile_setname(regular_user['token'], "Uncle", "Joe")
    profile = user_profile(regular_user['token'], regular_user['u_id'])
    assert profile['user']['name_first'] == "Uncle"
    assert profile['user']['name_last'] == "Joe"

    clear()

# input error when first name greater than 50 chars
def test_user_profile_setname_input_error_name_first_long():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setname(regular_user['token'], "Uncleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "Joe")


    clear()

# input error when first name less than 1 char
def test_user_profile_setname_input_error_name_first_short():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setname(regular_user['token'], "", "Joe")


    clear()

# input error when last name greater than 50 chars
def test_user_profile_setname_input_error_name_last_long():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setname(regular_user['token'], "Uncle", "Joeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")


    clear()

# input error when last name less than 1 char
def test_user_profile_setname_input_error_name_last_short():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setname(regular_user['token'], "Uncle", "")


    clear()

def test_user_profile_setemail_normal():
    clear()

    regular_user = register_user()

    user_profile_setemail(regular_user['token'], "NewEmail@gmail.com")
    
    profile = user_profile(regular_user['token'], regular_user['u_id'])
    assert profile['user']['email'] == "NewEmail@gmail.com"

    clear()


def test_user_profile_setemail_input_error_invalid_email():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setemail(regular_user['token'], "this_is_not_valid@gmail.com")


    clear()


def test_user_profile_setemail_input_error_emaily_already_used():
    clear()

    regular_user = register_user()
    auth_register("NewEmail@gmail.com", "valid_password", "Woopdidi", "Scoop")
    auth_login("NewEmail@gmail.com", "valid_password")

    with pytest.raises(InputError):
        user_profile_setemail(regular_user['token'], "NewEmail@gmail.com")


    clear()


def test_user_profile_sethandle_normal():
    clear()

    regular_user = register_user()

    user_profile_sethandle(regular_user['token'], "filler")
    
    profile = user_profile(regular_user['token'], regular_user['u_id'])
    assert profile['user']['handle_str'] == "filler"

    user_profile_sethandle(regular_user['token'], "Sykkuno")
    updated_profile = user_profile(regular_user['token'], regular_user['u_id'])
    assert updated_profile['user']['handle_str'] == "Sykkuno"


    clear()


def test_user_profile_sethandle_input_error_too_long():
    clear()
    
    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_sethandle(regular_user['token'], "loooooooooooooooooooooooooooong")


    clear()

def test_user_profile_sethandle_input_error_too_short():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_sethandle(regular_user['token'], "DQ")


    clear()



def test_user_profile_sethandle_input_error_already_used():
    clear()

    regular_user = register_user()

    user_profile_sethandle(regular_user['token'], "IYKYK")

    new_user = auth_register("NewEmail@gmail.com", "valid_password", "Woopdidi", "Scoop")
    auth_login("NewEmail@gmail.com", "valid_password")

    with pytest.raises(InputError):
        user_profile_sethandle(new_user['token'], "IYKYK")

    clear()