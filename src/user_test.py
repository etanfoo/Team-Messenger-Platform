import pytest
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile_uploadphoto
from auth import auth_login, auth_register, auth_register
from other import clear
from error import InputError

INVALID_U_ID = 99999999999

# function to register a user and log them in
def register_user():
    user = auth_register("validEmail@gmail.com", "valid_password", "Phil", "Knight")
    auth_login("validEmail@gmail.com", "valid_password")

    return user


def test_user_profile_normal():
    clear()

    regular_user = register_user()
    
    profile = user_profile(regular_user['token'], regular_user['u_id'])

    assert profile['user']['u_id'] == regular_user['u_id']
    assert profile['user']['email'] == "validEmail@gmail.com"
    assert profile['user']['name_first'] == "Phil"
    assert profile['user']['name_last'] == "Knight"
    assert profile['user']['handle_str'] == "philknight"

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
        user_profile_setname(regular_user['token'], "Uncle" * 20, "Joe")


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
        user_profile_setname(regular_user['token'], "Uncle", "Joe" * 20)


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

# input error when email > 254 char
def test_user_profile_setemail_input_error_email_too_long():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setemail(regular_user['token'], "long" * 100 + '@gmail.com')


    clear()

# inpuyt error when email == 0 char
def test_user_profile_setemail_input_error_email_too_short():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setemail(regular_user['token'], "")


    clear()




def test_user_profile_setemail_input_error_invalid_email():
    clear()

    regular_user = register_user()

    with pytest.raises(InputError):
        user_profile_setemail(regular_user['token'], "this_is_not_valid@gmail.com")


    clear()


def test_user_profile_setemail_input_error_email_already_used():
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
        user_profile_sethandle(regular_user['token'], "long" * 20)


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


def test_user_profile_uploadphoto_input_error_http_status():
    clear()

    regular_user = register_user()
    
    with pytest.raises(InputError):
        user_profile_uploadphoto(regular_user['token'], 'not_a_url_lmao', 0, 0, 200, 200)


def test_user_profile_uploadphoto_input_error_invalid_dimensions():
    clear()

    regular_user = register_user()
    
    with pytest.raises(InputError):
        user_profile_uploadphoto(regular_user['token'], 'https://i.imgur.com/b27q1.jpg', 500, 500, 0, 0)


def test_user_profile_uploadphoto_input_error_not_JPG():
    clear()

    regular_user = register_user()
    
    with pytest.raises(InputError):
        user_profile_uploadphoto(regular_user['token'], 'https://i.imgur.com/UO6M4.png', 0, 0, 200, 200)

    
# def test_user_profile_uploadphoto_normal():
#     clear()

#     regular_user = register_user()

#     user_profile_uploadphoto(regular_user['token'], 'https://i.imgur.com/b27q1.jpg', 0, 0, 200, 200)
