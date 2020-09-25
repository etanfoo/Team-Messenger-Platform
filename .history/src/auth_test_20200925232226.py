import pytest
from error import InputError, AccessError
#Test Login

#Check for valid Email
#Email entered does not belong to a user
#Password is not correct
def test_login():
    assert auth_login(email, password) 


#Test Register

#Check for valid Email
def test_register_email():
    with pytest.raises(InputError):
        auth_register("gilbertzhuo@gmail.com", "Test@12345", "Gilbert", "Zhuo")
 
        
#Check if email has already been used by another user

#Pasword entered is less than 6 characters
def test_register_password_length():
    with pytest.raises(InputError):
        auth_register("gilbertzhuo@gmail.com", "12345", "Gilbert", "Zhuo")

#Password is not empty
def test_register_password_empty():
    with pytest.raises(InputError):
        auth_register("gilbertzhuo@gmail.com", "Test@12345", "Gilbert", "Zhuo")

#name_first is not between 1 and 50 characthers
def test_register_name_first_empty():
    with pytest.raises(InputError):
         auth_register("gilbertzhuo@gmail.com", "Test@12345", "", "Zhuo")

#name_last is not between 1 and 50 characters in length
def test_register_name_last_empty():
    with pytest.raises(InputError):
         auth_register("gilbertzhuo@gmail.com", "Test@12345", "Gilbert", "This")
