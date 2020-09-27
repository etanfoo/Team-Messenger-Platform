import pytest
from error import InputError, AccessError
from auth import auth_register, auth_login

########################
######Test Login#######
#######################

#Check login
def test_login_email():
    auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # Expect to work since we registered
    auth_login('validemail@gmail.com', '123abc!@#')
    
    with pytest.raises(InputError) as e:
        auth_login('didntusethis@gmail.com', '123abcd!@#')

#Check password
def test_login_password():
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError) as e:
        auth_login('validemail@gmail.com', 'thisIsTheWrongPassword')

#Email address cannot exceed 254 characters
def test_login_email_limit():
    with pytest.raises(InputError) as e:
        auth_login("atestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatest@gmail.com ", "Test@12345")

#Email address first character of username must be an ascii letter (a-z) or number (0-9)
def test_login_email_first_letter():
    with pytest.raises(InputError) as e:
        auth_login(".atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("~atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("!atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("#atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("$atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("^atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("&atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("*atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("(atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login(")atest@gmail.com ", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("+atest@gmail.com ", "Test@12345")
#Email address cannot have a leading space 
def test_login_email_space_leading():
    with pytest.raises(InputError) as e:
        auth_login("atest@gmail.com ", "Test@12345")
def test_login_email_space_trailing():
    with pytest.raises(InputError) as e:
        auth_login("a test@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("atest@gm ail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("atest@gmail. com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("atest@gmail.c om", "Test@12345")
#Email address username can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_login_email_username():
    with pytest.raises(InputError) as e:
        auth_login("a!test@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("a.te-st@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("ate\st@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("ates]t@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("ates$@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("at#es@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("at~es@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("at-es@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("at*es@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("at&es@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("at_es@gmail.com", "Test@12345")

#Email address domain can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_login_email_domain():
    with pytest.raises(InputError) as e:
        auth_login("a!test@a!test.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@a.te-st.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@ate\st.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@ates]t.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@ates$.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@at#es.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@at~es.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@at-es.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@at*es.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@at&es.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("test@at_es.com", "Test@12345")

#Email address cannot contain consecutive periods (.)
def test_login_email_period():
    with pytest.raises(InputError) as e:
        auth_login("dummy..test@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("dummytest..@gmail.com", "Test@12345")
#Email address domain cannot be localhost
def test_login_localhost():
    with pytest.raises(InputError) as e:
        auth_login("dummytest@localhost.com", "Test@12345")

#Email address cannot contain more than 1 "@"
def test_login_email():
    with pytest.raises(InputError) as e:
        auth_login("dummy@test@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("@dummytest@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("dummytest@@gmail.com", "Test@12345")
    with pytest.raises(InputError) as e:
        auth_login("dummytest@gmail.com@", "Test@12345")

#Email address must contain 1 "@"
def test_login_email_1():
    with pytest.raises(InputError) as e:
         auth_login("dummy.com", "Test@12345")
    with pytest.raises(InputError) as e:
         auth_login("dummytest.com", "Test@12345")

#Email address must have a domain after the @ sign
def test_login_email_domain():
    with pytest.raises(InputError) as e:
        auth_login("dummytest@", "test@12345")
    with pytest.raises(InputError) as e:
        auth_login("apple.bottom.jeans@", "test@12345")

#Password entered is more than 18 characthers
def test_login_password_max():
    with pytest.raises(InputError) as e:
        auth_login("dummytest@gmail.com", "ThisIsAReallyLongSentenceThisIsAReallyLongSentence")
    with pytest.raises(InputError) as e:
        auth_login("dummytest@gmail.com", "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    with pytest.raises(InputError) as e:
        auth_login("dummytest@gmail.com", "111111111111111111111111111111111111111111111111111")
        
#Pasword entered is less than 6 characters
def test_login_password_min():
    with pytest.raises(InputError) as e:
        auth_login("dummytest@gmail.com", "12345")
    with pytest.raises(InputError) as e:
        auth_login("dummytest@gmail.com", "12o45")

#Email is not empty 
def test_login_email_empty():
    with pytest.raises(InputError) as e:
        auth_login("", "Test@12345")

#Password is not empty
def test_login_password_empty():
    with pytest.raises(InputError) as e:
        auth_login("DummyTest@gmail.com", "")


########################
#Check for valid Email#
#######################
#Check if email has already been used by another user
def test_register_check_user():
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')


#Email address cannot exceed 254 characters
def test_register_email_limit():
    with pytest.raises(InputError) as e:
        auth_register("atestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatestatest@gmail.com ", "Test@12345", "Dummy", "Test")

#Email address first character of username must be an ascii letter (a-z) or number (0-9)
def test_register_email_first_letter():
    with pytest.raises(InputError) as e:
        auth_register(".atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("~atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("!atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("#atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("$atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("^atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("&atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("*atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("(atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register(")atest@gmail.com ", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("+atest@gmail.com ", "Test@12345", "Dummy", "Test")
#Email address cannot have a leading space 
def test_register_email_space_leading():
    with pytest.raises(InputError) as e:
        auth_register("atest@gmail.com ", "Test@12345", "Dummy", "Test")
def test_register_email_space_trailing():
    with pytest.raises(InputError) as e:
        auth_register("a test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("atest@gm ail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("atest@gmail. com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("atest@gmail.c om", "Test@12345", "Dummy", "Test")
#Email address username can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_register_email_username():
    with pytest.raises(InputError) as e:
        auth_register("a!test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("a.te-st@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("ate\st@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("ates]t@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("ates$@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("at#es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("at~es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("at-es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("at*es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("at&es@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("at_es@gmail.com", "Test@12345", "Dummy", "Test")

#Email address domain can only contain letters (a-z), numbers (0-9) and periods (.) are allowed
def test_register_email_domain():
    with pytest.raises(InputError) as e:
        auth_register("a!test@a!test.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@a.te-st.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@ate\st.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@ates]t.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@ates$.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@at#es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@at~es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@at-es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@at*es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@at&es.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("test@at_es.com", "Test@12345", "Dummy", "Test")

#Email address cannot contain consecutive periods (.)
def test_register_email_period():
    with pytest.raises(InputError) as e:
        auth_register("dummy..test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("dummytest..@gmail.com", "Test@12345", "Dummy", "Test")
#Email address domain cannot be localhost
def test_register_localhost():
    with pytest.raises(InputError) as e:
        auth_register("dummytest@localhost.com", "Test@12345", "Dummy", "Test")

#Email address cannot contain more than 1 "@"
def test_register_email():
    with pytest.raises(InputError) as e:
        auth_register("dummy@test@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("@dummytest@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("dummytest@@gmail.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("dummytest@gmail.com@", "Test@12345", "Dummy", "Test")

#Email address must contain 1 "@"
def test_register_email_1():
    with pytest.raises(InputError) as e:
         auth_register("dummy.com", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
         auth_register("dummytest.com", "Test@12345", "Dummy", "Test")

#Email address must have a domain after the @ sign
def test_register_email_domain():
    with pytest.raises(InputError) as e:
        auth_register("dummytest@", "Test@12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("apple.bottom.jeans@", "Test@12345", "Dummy", "Test")

#Password entered is more than 18 characthers
def test_register_password_max():
    with pytest.raises(InputError) as e:
        auth_register("dummytest@gmail.com", "ThisIsAReallyLongSentenceThisIsAReallyLongSentence", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("dummytest@gmail.com", "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("dummytest@gmail.com", "111111111111111111111111111111111111111111111111111", "Dummy", "Test")
        
#Pasword entered is less than 6 characters
def test_register_password_min():
    with pytest.raises(InputError) as e:
        auth_register("dummytest@gmail.com", "12345", "Dummy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("dummytest@gmail.com", "12o45", "Dummy", "Test")

#Email is not empty 
def test_register_email_empty():
    with pytest.raises(InputError) as e:
        auth_register("", "Test@12345", "Dummy", "Test")

#Password is not empty
def test_register_password_empty():
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "", "Dummy", "Test")

#First name is not empty
def test_register_name_first_empty():
    with pytest.raises(InputError) as e:
         auth_register("DummyTest@gmail.com", "Test@12345", "", "Test")

#Last name is not empty
def test_register_name_last_empty():
    with pytest.raises(InputError) as e:
         auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "")

#name_first is not between 1 and 50 characthers
def test_register_name_first_50():
    with pytest.raises(InputError) as e:
         auth_register("DummyTest@gmail.com", "Test@12345", "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname", "Test")

#name_last is not between 1 and 50 characters in length
def test_register_name_last_50():
    with pytest.raises(InputError) as e:
         auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "ThisisaverylonglastnameThisisaverylonglastnameThisisaverylonglastname")

def test_register_name_first_symbol():
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy@", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum!my", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum#my", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dumm$y", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum^my", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum&my", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Du*mmy", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum(my", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dumm)y", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dum-my", "Test")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dumm=y", "Test")

def test_register_name_last_symbol():
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes!t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes@t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes#t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes$t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Test%")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes^t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes&t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes*t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes(t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes)t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Tes-t")
    with pytest.raises(InputError) as e:
        auth_register("DummyTest@gmail.com", "Test@12345", "Dummy", "Test=")

    