from error import InputError
import pytest

def test_channels_list():
    assert channels_list(authorised_user['token']) == smth

def test_channels_listall():
    assert channels_listall(authorised_user['token']) == smth

def test_channels_create():
     with pytest.raises(InputError):   
        # Expected to fail, Channel name is over 20 characters long (no spaces)
        channels_create(authorised_user['token'], "ThisIsATestForALongChannelName", True)

    with pytest.raises(InputError):   
        # Expected to fail, Channel name is over 20 characters long
        channels_create(authorised_user['token'], "The Kanye East experience", False)
