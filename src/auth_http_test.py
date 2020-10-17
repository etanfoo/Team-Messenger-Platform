import pytest
import requests
import json
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from error import InputError, AccessError
import pytest

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

user = {
    "email": "validEmail@gmail.com",
    "password": "valid_password",
    "name_first": "Phil",
    "name_last": "Knight",
}

#Check login
def test_login_email_nonexist(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "didntusethis@gmail.com",
            "password": "123abcd!@#"
        })

#Check password
def test_login_password(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    requests.post(f"{url}/auth/register", json = user)
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "validEmail@gmail.com",
            "password": "thisIsTheWrongPassword"
        })

#Email address cannot exceed 254 characters
def test_login_email_limit(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "atestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatest@gmail.com",
            "password": "Test@12345"
        })

#Email address first character of username must be an ascii letter (a-z) or number (0-9)
def test_login_email_first_letter(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": ".atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "~atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "!atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "#atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "$atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "^atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "&atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "*atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "(atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": ")atest@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "+atest@gmail.com",
            "password": "Test@12345"
        })

    
#Email address cannot have any white spaces 
def test_login_email_space_trailing(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "atest@gmail.com ",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "a test@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "atest@gm ail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "atest@gmail. com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "atest@gmail.c om",
            "password": "Test@12345"
        })
    

#Email address username can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_login_email_username(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "a!test@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "a.te-st@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "ates]t@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "ates$@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "at#es@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "at~es@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "at-es@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "at*es@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "at&es@gmail.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "at_es@gmail.com",
            "password": "Test@12345"
        })

#Email address domain can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_login_email_domain1(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "atest@a!test.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@a.te-st.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@ates]t.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@ates$.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@at#es.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@at~es.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@at-es.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@at*es.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@at&es.com",
            "password": "Test@12345"
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/login", json = {
            "email": "test@at_es.com",
            "password": "Test@12345"
        })

#Email address cannot contain consecutive periods (.)
def test_login_email_period(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummy..test@gmail.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest..@gmail.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Email address domain cannot be localhost
def test_register_localhost(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@localhost.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Email address cannot contain more than 1 "@"
def test_register_email(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummy@test@gmail.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "@dummytest@gmail.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@@gmail.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com@",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Email address must contain 1 "@"
def test_register_email_1(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummy.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest.com",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Email address must have a domain after the @ sign
def test_register_email_domain(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "apple.bottom.jeans@",
            "password": "valid_password",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Password entered is more than 18 characthers
def test_register_password_max(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "ThisIsAReallyLongSentenceThisIsAReallyLongSentence",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "111111111111111111111111111111111111111111111111111",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Pasword entered is less than 6 characters
def test_register_password_min(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "12345",
            "name_first": "Phil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "12o45",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Email is not empty
def test_register_email_empty(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#Password is not empty
def test_register_password_empty(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "",
            "name_first": "Phil",
            "name_last": "Knight",
        })

#First name is not empty
def test_register_name_first_empty(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "",
            "name_last": "Knight",
        })

#Last name is not empty
def test_register_name_last_empty(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "",
        })

#name_first is not between 1 and 50 characthers
def test_register_name_first_50(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname",
            "name_last": "Knight",
        })

#name_last is not between 1 and 50 characters in length
def test_register_name_last_50(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname",
        })

def test_register_name_first_symbol(url):
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil@",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phi!l",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Ph#il",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "P$hil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Ph^il",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Ph&il",
            "name_last": "Knight",
        })
    
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phi*l",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "P(hil",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phi)l",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Ph-il",
            "name_last": "Knight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "P=hil",
            "name_last": "Knight",
        })

def test_register_name_last_symbol():
    # Reset/clear data
    requests.delete(f"{url}/clear")
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Kn!ight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Knigh@t",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Kni#ght",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "K$night",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Knigh%t",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Kn^ight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Kni&ght",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Knigh*t",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Kn(ight",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "K)night",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "Kni-ght",
        })
    with pytest.raises(InputError):
        requests.post(f"{url}/auth/register", json = {
            "email": "dummytest@gmail.com",
            "password": "Test@12345",
            "name_first": "Phil",
            "name_last": "K=night",
        })
