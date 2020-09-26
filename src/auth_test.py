import pytest
from error import InputError, AccessError
from auth.py import *
#Test Login

#Check for valid Email
#Email entered does not belong to a user
#Password is not correct

#-------------------------------------------------------------------
########################
#Check for valid Email#
#######################
#Check if email has already been used by another user
#--------#
#Email address cannot exceed 254 characters
def test_register_email_limit():
    with pytest.raises(InputError):
        auth_register("atestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatest@gmail.com ", "Test@12345", "Dummy", "Test")


#Email address first character of username must be an ascii letter (a-z) or number (0-9)
def test_register_email_first_letter():
    with pytest.raises(InputError):
        auth_register(".atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("~atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("!atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("#atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("$atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("^atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("&atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("*atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("(atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register(")atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("+atest@gmail.com ", "Test@12345", "Dummy", "Test")
#Email address cannot have a leading space 
def test_register_email_space_leading():
    with pytest.raises(InputError):
        auth_register("atest@gmail.com ", "Test@12345", "Dummy", "Test")
def test_register_email_space_trailing():
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
    with pytest.raises(InputError):
        auth_register("a!test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("a.te-st@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("ate\st@gmail.com", "Test@12345", "Dummy", "Test")
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
def test_register_email_domain():
    with pytest.raises(InputError):
        auth_register("a!test@a!test.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@a.te-st.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("test@ate\st.com", "Test@12345", "Dummy", "Test")
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
    with pytest.raises(InputError):
        auth_register("dummy..test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest..@gmail.com", "Test@12345", "Dummy", "Test")
#Email address domain cannot be localhost
def test_register_localhost():
    with pytest.raises(InputError):
        auth_register("dummytest@localhost.com", "Test@12345", "Dummy", "Test")

#Email address cannot contain more than 1 "@"
def test_register_email():
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
    with pytest.raises(InputError):
         auth_register("dummy.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError):
         auth_register("dummytest.com", "Test@12345", "Dummy", "Test")

#Email address must have a domain after the @ sign
def test_register_email_domain():
    with pytest.raises(InputError):
        auth_register("dummytest@")
    with pytest.raises(InputError):
        auth_register("apple.bottom.jeans@")

#Password entered is more than 18 characthers
def test_register_password_max():
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com", "ThisIsAReallyLongSentenceThisIsAReallyLongSentence", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com", "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com", "111111111111111111111111111111111111111111111111111", "Dummy", "Test")
        
#Pasword entered is less than 6 characters
def test_register_password_min():
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com", "12345", "Dummy", "Test")
    with pytest.raises(InputError):
        auth_register("dummytest@gmail.com", "12o45", "Dummy", "Test")

#Email is not empty 
def test_register_email_empty():
    with pytest.raises(InputError):
        auth_register("", "Test@12345", "Dummy", "Test")

#Password is not empty
def test_register_password_empty():
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "", "Dummy", "Test")

#First name is not empty
def test_register_name_first_empty():
    with pytest.raises(InputError):
         auth_register("DummyTest@gmail.com", "Test@12345", "", "Test")

#Last name is not empty
def test_register_name_last_empty():
    with pytest.raises(InputError):
         auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "")

#name_first is not between 1 and 50 characthers
def test_register_name_first_50():
    with pytest.raises(InputError):
         auth_register("DummyTest@gmail.com", "Test@12345", "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname", "Test")

#name_last is not between 1 and 50 characters in length
def test_register_name_last_50():
    with pytest.raises(InputError):
         auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname")

def test_register_name_first_symbol():
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy@", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum!my", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum#my", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dumm$y", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum^my", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum&my", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Du*mmy", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum(my", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dumm)y", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum-my", "Test")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dumm=y", "Test")

def test_register_name_last_symbol():
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes!t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes@t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes#t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes$t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Test%")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes^t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes&t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes*t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes(t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes)t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes-t")
    with pytest.raises(InputError):
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Test=")

    