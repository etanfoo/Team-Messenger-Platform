'''
AUTH_HTTP
'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest
import requests
from utils import register_user_auth, login_user, user_details, passwordreset_request


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


###################
# Global variables
###################

user = {
    "email": "validEmail@gmail.com",
    "password": "valid_password",
    "name_first": "Phil",
    "name_last": "Knight",
}


def test_login_email_nonexist(url):
    '''
    An email that does not exist in the database
    '''
    payload = login_user(url,
                         user_details("didntusethis@gmail.com", "123abcd!@#"))
    assert payload.status_code == 400


def test_login_password(url):
    '''
    An incorrect password
    '''
    payload = login_user(
        url, user_details("validEmail@gmail.com", "thisIsTheWrongPassword"))
    assert payload.status_code == 400


def test_login_email_limit(url):
    '''
    An email that exceed 254 characters
    '''
    payload = login_user(
        url, user_details("a" * 255 + "@hotmail.com", "Test@12345"))
    assert payload.status_code == 400


def test_login_email_first_letter(url):
    '''
    Email addresses with first character not
    being an ascii letter (a-z) or number (0-9)
    '''
    payload = login_user(url, user_details(".atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("~atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("!atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("#atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("$atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("&atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("*atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("(atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details(")atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("+atest@gmail.com", "Test@12345"))
    assert payload.status_code == 400


def test_login_email_space_trailing(url):
    '''
    Email addresses a whitespace in-between
    '''
    payload = login_user(url, user_details("atest@gmail.com ", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("a test@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("atest@gm ail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("atest@gmail. com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("atest@gmail.c om", "Test@12345"))
    assert payload.status_code == 400


def test_login_email_username(url):
    '''
    Email addresses that contains a special symbol in the username section
    '''
    payload = login_user(url, user_details("a!test@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("a.te-st@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("ates]t@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("ates$@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("at#es@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("at~es@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("at-es@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("at*es@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("at&es@gmail.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("at_es@gmail.com", "Test@12345"))
    assert payload.status_code == 400


def test_login_email_domain1(url):
    '''
    Email addresses that contains a special symbol in the domain section
    '''
    payload = login_user(url, user_details("atest@a!test.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@a.te-st.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@ates]t.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@ates$.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@at#es.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@at~es.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@at-es.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@at*es.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@at&es.com", "Test@12345"))
    assert payload.status_code == 400
    payload = login_user(url, user_details("test@at_es.com", "Test@12345"))
    assert payload.status_code == 400


def test_login_email_period(url):
    '''
    Email addresses that contains consecutive periods
    '''
    user["email"] = "dummy..test@gmail.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["email"] = "dummytest..@gmail.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_localhost(url):
    '''
    Email address's domain being localhost
    '''
    user["email"] = "dummytest@localhost.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_email(url):
    '''
    Email addresses containing more than one "@"
    '''
    user["email"] = "dummy@test@gmail.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["email"] = "@dummytest@gmail.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["email"] = "dummytest@@gmail.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["email"] = "dummytest@gmail.com@"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_email_1(url):
    '''
    Email addresses that does not contain one "@"
    '''
    user["email"] = "dummy.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["email"] = "dummytest.com"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_email_domain(url):
    '''
    Email addresses that does not contain a domain
    '''
    user["email"] = "dummytest@"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["email"] = "apple.bottom.jeans@"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_password_max(url):
    '''
    Passwords that exceeds 18 characters
    '''
    user["password"] = "ThisIsAReallyLongSentenceThisIsAReallyLongSentence"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["password"] = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["password"] = "111111111111111111111111111111111111111111111111111"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_password_min(url):
    '''
    Passwords that are less that 6 characters long
    '''
    user["password"] = "12345"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["password"] = "12o45"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_email_empty(url):
    '''
    Email that is empty
    '''
    user["email"] = ""
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_password_empty(url):
    '''
    Password that is empty
    '''
    user["password"] = ""
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_name_first_empty(url):
    '''
    First name that is empty
    '''
    user["name_first"] = ""
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_name_last_empty(url):
    '''
    Last name that is empty
    '''
    requests.delete(f"{url}/clear")
    user["name_last"] = ""
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_name_first_50(url):
    '''
    First name exceeds 50 characters
    '''
    user[
        "name_first"] = "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_name_last_50(url):
    '''
    Last name exceeds 50 characters
    '''
    user[
        "name_last"] = "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_name_first_symbol(url):
    '''
    First name contains a special symbol
    '''
    user["name_first"] = "Phil@"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "Phi!l"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "Ph#il"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "P$hil"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "Ph^il"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "Ph&il"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "Phi*l"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "P(hil"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "Phi)l"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "Ph-il"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_first"] = "P=hil"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400


def test_register_name_last_symbol(url):
    '''
    Last name contains a special symbol
    '''
    user["name_last"] = "Kn!ight"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Knigh@t"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Kni#ght"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "K$night"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Knigh%t"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Kn^ight"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Kni&ght"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Knigh*t"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Kn(ight"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "K)night"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "Kni-ght"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

    user["name_last"] = "K=night"
    payload = register_user_auth(url, user)
    assert payload.status_code == 400

def test_request_invalid_emails(url):
    '''
    The emails are invalid or not in the database
    '''    
    payload = passwordreset_request(url, "INVALID_EMAIL@gmail.com")
    assert payload.status_code == 400

    payload = passwordreset_request(url, "ThisIsNotAEmail")
    assert payload.status_code == 400

def test_request_integers()
    '''
    The email is invalid as it is integers
    '''
    payload = passwordreset_request(url, 2118)
    assert payload.status_code == 400

def test_request_empty()
    '''
    No email provided
    '''
    payload = passwordreset_request(url, "")
    assert payload.status_code == 400

def test_request_white_spaces()
    '''
    Email provided are white spaces
    '''
    payload = passwordreset_request(url, "      ")
    assert payload.status_code == 400