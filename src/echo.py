'''
Echo.py
'''
from error import InputError


def echo(value):
    '''
    Echo value
    '''
    if value == 'echo':
        raise InputError('Input cannot be echo')
    return value
