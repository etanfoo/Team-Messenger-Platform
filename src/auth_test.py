'''
AUTH_TEST
'''
import pytest
from error import InputError, AccessError
from auth import auth_register, auth_login, auth_logout, auth_passwordreset_request
from other import clear

########################
######Test Login#######
#######################


#Check login
def test_login_email_nonexist():
    '''
    An email that does not exist in the database
    '''
    clear()
    with pytest.raises(InputError):
        auth_login('didntusethis@gmail.com', '123abcd!@#')


#Check password
def test_login_password():
    '''
    An incorrect password
    '''
    clear()
    auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth_login('validemail@gmail.com', 'thisIsTheWrongPassword')


#Email address cannot exceed 254 characters
def test_login_email_limit():
    '''
    An email that exceed 254 characters
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("a" * 255 + "@hotmail.com", "password")


#Email address first character of username must be an ascii letter (a-z) or number (0-9)
def test_login_email_first_letter():
    '''
    Email addresses with first character not
    being an ascii letter (a-z) or number (0-9)
    '''
    clear()
    with pytest.raises(InputError):
        auth_login(".atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("~atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("!atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("#atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("$atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("^atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("&atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("*atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("(atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login(")atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError):
        auth_login("+atest@gmail.com ", "Test@12345")


#Email address cannot have a leading space
def test_login_email_space_leading():
    '''
    Email addresses ending with whitespace
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("atest@gmail.com ", "Test@12345")


def test_login_email_space_trailing():
    '''
    Email addresses a whitespace in-between
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("a test@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("atest@gm ail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("atest@gmail. com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("atest@gmail.c om", "Test@12345")


#Email address username can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_login_email_username():
    '''
    Email addresses that contains a special symbol in the username section
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("a!test@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("a.te-st@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("ates]t@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("ates$@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("at#es@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("at~es@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("at-es@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("at*es@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("at&es@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("at_es@gmail.com", "Test@12345")


#Email address domain can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_login_email_domain1():
    '''
    Email addresses that contains a special symbol in the domain section
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("atest@a!test.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@a.te-st.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@ates]t.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@ates$.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@at#es.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@at~es.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@at-es.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@at*es.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@at&es.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("test@at_es.com", "Test@12345")


#Email address cannot contain consecutive periods (.)
def test_login_email_period():
    '''
    Email addresses that contains consecutive periods
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("dummy..test@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("dummytest..@gmail.com", "Test@12345")


#Email address domain cannot be localhost
def test_login_localhost():
    '''
    Email address's domain being localhost
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("dummytest@localhost.com", "Test@12345")


#Email address cannot contain more than 1 "@"
def test_login_email():
    '''
    Email addresses containing more than one "@"
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("dummy@test@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("@dummytest@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("dummytest@@gmail.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("dummytest@gmail.com@", "Test@12345")


#Email address must contain 1 "@"
def test_login_email_1():
    '''
    Email addresses that does not contain one "@"
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("dummy.com", "Test@12345")
    with pytest.raises(InputError):
        auth_login("dummytest.com", "Test@12345")


#Email address must have a domain after the @ sign
def test_login_email_domain():
    '''
    Email addresses that does not contain a domain
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("dummytest@", "test@12345")
    with pytest.raises(InputError):
        auth_login("apple.bottom.jeans@", "test@12345")


#Email is not empty
def test_login_email_empty():
    '''
    Email empty
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("", "Test@12345")


#Password is not empty
def test_login_password_empty():
    '''
    Passwords empty
    '''
    clear()
    with pytest.raises(InputError):
        auth_login("DummyTest@gmail.com", "")


########################
#Check for valid Email#
#######################


def test_register_check_user():
    '''
    Check if email has already been used by another user
    '''
    clear()
    auth_register('validemailthx@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth_register('validemailthx@gmail.com', '123abc!@#', 'Hayden',
                      'Everest')


#Email address cannot exceed 254 characters
def test_register_email_limit():
    '''
    Email address cannot exceed 254 characters
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("a" * 255 + "@hotmail.com", "password", "Dummy", "Test")


#Email address first character of username must be an ascii letter (a-z) or number (0-9)
def test_register_email_first_letter():
    '''
    Email address first character of username must be an ascii letter (a-z) or number (0-9)
    '''
    clear()
    with pytest.raises(InputError):
        auth_register(".atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("~atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("!atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("#atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("$atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("^atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("&atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("*atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("(atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register(")atest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("+atest@gmail.com", "Test@12345", "Dummy", "Test")


#Email address cannot have a leading space
def test_register_email_space_leading():
    '''
    Email address cannot have a leading space
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("atest@gmail.com ", "Test@12345", "Dummy", "Test")


def test_register_email_space_trailing():
    '''
    Email address cannot have a trailing space
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("a test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("atest@gm ail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("atest@gmail. com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("atest@gmail.c om", "Test@12345", "Dummy", "Test")


#Email address username can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_register_email_username():
    '''
    Email address username can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("a!test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("a.te-st@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("ates]t@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("ates$@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("at#es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("at~es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("at-es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("at*es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("at&es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("at_es@gmail.com", "Test@12345", "Dummy", "Test")


#Email address domain can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_register_email_domain1():
    '''
    Email address username can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("a!test@a!test.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@a.te-st.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@ates]t.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@ates$.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@at#es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@at~es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@at-es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@at*es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@at&es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@at_es.com", "Test@12345", "Dummy", "Test")


#Email address cannot contain consecutive periods (.)
def test_register_email_period():
    '''
    Email address cannot contain consecutive periods (.)
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("dummy..test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest..@gmail.com", "Test@12345", "Dummy", "Test")


#Email address domain cannot be localhost
def test_register_localhost():
    '''
    Email address domain cannot be localhost
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("dummytest@localhost.com", "Test@12345", "Dummy", "Test")


#Email address cannot contain more than 1 "@"
def test_register_email():
    '''
    Email address cannot contain more than 1 "@"
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("dummy@test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("@dummytest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com@", "Test@12345", "Dummy", "Test")


#Email address must contain 1 "@"
def test_register_email_1():
    '''
    Email address cannot contain more than 1 "@"
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("dummy.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest.com", "Test@12345", "Dummy", "Test")


#Email address must have a domain after the @ sign
def test_register_email_domain():
    '''
    Email address must have a domain after the @ sign
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("dummytest@", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("apple.bottom.jeans@", "Test@12345", "Dummy", "Test")


#Password entered is more than 18 characthers
def test_register_password_max():
    '''
    Password entered is more than 18 characthers
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com",
                      "ThisIsAReallyLongSentenceThisIsAReallyLongSentence",
                      "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com",
                      "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
                      "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com",
                      "111111111111111111111111111111111111111111111111111",
                      "Dummy", "Test")


#Pasword entered is less than 6 characters
def test_register_password_min():
    '''
    Pasword entered is less than 6 characters
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com", "12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com", "12o45", "Dummy", "Test")


#Email is not empty
def test_register_email_empty():
    '''
    Email is not empty
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("", "Test@12345", "Dummy", "Test")


#Password is not empty
def test_register_password_empty():
    '''
    Pasword is not empty
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "", "Dummy", "Test")


#First name is not empty
def test_register_name_first_empty():
    '''
    First name is not empty
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "", "Test")


#Last name is not empty
def test_register_name_last_empty():
    '''
    Last name is not empty
    '''
    clear()
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "")


#name_first is not between 1 and 50 characthers
def test_register_name_first_50():
    '''
    first name is not between 1 and 50 characthers
    '''
    clear()
    with pytest.raises(InputError):
        auth_register(
            "DummyTest@gmail.com", "Test@12345",
            "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname",
            "Test")


#name_last is not between 1 and 50 characters in length
def test_register_name_last_50():
    '''
    last name is not between 1 and 50 characters in length
    '''
    clear()
    with pytest.raises(InputError):
        auth_register(
            "DummyTest@gmail.com", "Test@12345", "Dummy",
            "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname"
        )

def test_request_invalid_emails():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_request("INVALID_EMAIL@gmail.com")
    with pytest.raises(InputError):
        auth_passwordreset_request("ThisIsNotAEmail")    

def test_request_integers():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_request(2118)

def test_request_empty():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_request("")

def test_request_white_spaces():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_request("     ")
