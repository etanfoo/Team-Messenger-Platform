'''
Channel Helper
'''

from error import InputError


def valid_channel_name(name):
    '''
    Check name to be valid length
    '''
    if len(name) > 20 or len(name) < 1 or name.isspace():
        raise InputError(
            "Channel name must consist of 1 to 20 characters long.")
