from utils import decode_token


def valid_channel_name(name):
    if len(name) > 20 or name == '' or name.isspace():
        raise InputError