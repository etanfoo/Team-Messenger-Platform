'''
Echo Test
'''
import echo
import pytest
from error import InputError


def test_echo():
    '''
    Test Echo
    '''
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"


def test_echo_except():
    '''
    Echo return expect
    '''
    with pytest.raises(InputError):
        assert echo.echo("echo")
