import pytest
#Test Login
def test_login():
    assert auth_login(email, password) 

#Test Logout
def test_logout():
    assert auth_logout(token)


#Test Register
def test_register():
    assert auth_register(email, password, name_first, name_last)