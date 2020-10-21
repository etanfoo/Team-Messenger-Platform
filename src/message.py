from error import InputError, AccessError


def message_send(token, channel_id, message):
    if (len(message) > 1000):
        raise InputError(InputError)

    return {
        'message_id': 1,
    }


def message_remove(token, message_id):

    return {}


def message_edit(token, message_id, message):
    if (len(message) > 1000):
        raise InputError(InputError)

    return {}
