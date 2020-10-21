from datetime import datetime
from jwt import encode, decode, InvalidTokenError
from appsecret import JWT_SECRET


def generate_token(user_id):
    '''
    Returns a JWT token based on the users id and a secret message.
    '''
    token = jwt.encode({
        'user_id': user_id,
    }, JWT_SECRET, algorithm='HS256').decode('UTF-8')
    return token


def decode_token(token):
    '''
    decode_token
    '''
    decoded = jwt.decode(token, JWT_SECRET, algorithms='HS256')
