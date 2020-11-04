'''
standup functionality.
once standups are finished, all messages sent to standup/send are packaged together in a single messaged
and posted by the user who begun the standup/
'''

def standup_start(token, channel_id, length):
 
    return {'time_finish': 'time_finish'}


def standup_active(token, channel_id):

    return {'is_active': 'is_active', 'time_finish': 'time_finish'}


def standup_send(token, channel_id, message):
    return 0