from datetime import datetime
import jwt
from appsecret import JWT_SECRET
from error import AccessError
from global_dic import data


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
    return jwt.decode(token, JWT_SECRET, algorithms='HS256')['user_id']


def check_token(token):
    '''
    Checks if a jwt token corresponds to a currently logged in user.
    If the user's account has been deleted, invalidates that users token.
    :param token: jwt token
    :type token: str
    :raises AccessError: If the token does not correspond to a logged in user
    :raises AccessError: If the token corresponds to a deleted user
    :return: User id corresponding to the the valid token
    :rtype: int
    '''
    for i in range(len(data["users"])):
        #Find token
        if (data["users"][i]["token"] == token):
            return True
    #Token does not exist
    raise AccessError(description="Token does not exist")


def remove_token(token):
    for i in range(len(data["users"])):
        #Find token
        if (data["users"][i]["token"] == token):
            del data["users"][i]["token"]
            return True
<<<<<<< HEAD
    #Token does not exist
    raise AccessError(description="Token does not exist")
=======
    return False


if __name__ == "__main__":
    print(decode_token(generate_token("gilbert")))
>>>>>>> it2_dev
