from global_dic import data
from auth import auth_login, auth_register, auth_register
from error import InputError
import uuid
import re
from utils import check_token, random_string, get_user_from_token
import urllib.request
from PIL import Image
from flask import request as Flask_request

def valid_u_id_check(u_id):
    '''
    a function to raise input errors for invalid users
    '''
    # looping to see if u_id is a valid user, if not, input error
    found = False
    for user in data['users']:
        if u_id == user['u_id']:
            found = True
            break
    if found == False:
        raise InputError


def user_profile(token, u_id):
    '''
    For a valid user, returns information about their email, 
    first name, last name, and handle
    '''
    
    valid_u_id_check(u_id)
    check_token(token)

    # looping until we match the u_id in the global data structure
    for user in data['users']:
        if u_id == user['u_id']:
            # returning the required data
            return {
                'user': {
                    'u_id': user['u_id'],
                    'email': user['email'],
                    'name_first': user['first_name'],
                    'name_last': user['last_name'],
                    'handle_str': user['handle'],
                    'profile_img_url': user['profile_img_url']
                 },
            }


def user_profile_setname(token, name_first, name_last):
    '''
    Update the authorised user's first and last name
    '''
    check_token(token)

    # input error checking
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError
    
    # looping until we reach the user with corresponding token
    # and changing their respective first/last name
    for user in data['users']:
        if token == user['token']:
            user['first_name'] = name_first
            user['last_name'] = name_last
            break

    # changing user name in the channels they are part of
    for channel in data['channels']:
        for member in channel['all_members']:
            if user['u_id'] == member['u_id']:
                member['name_first'] = name_first
                member['name_last'] = name_last
        for member in channel['owner_members']:
            if user['u_id'] == member['u_id']:
                member['name_first'] = name_first
                member['name_last'] = name_last
    

    return {
    }

def user_profile_setemail(token, email):
    '''
    Update the authorised user's email address
    '''

    check_token(token)

    # using the same email pattern as auth_login
    emailPattern = "^(?!.*[.]{2})[a-zA-Z0-9][a-zA-Z0-9.]+@(?!localhost)[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"
    if len(email) > 254:
        raise InputError
    if len(email) == 0:
        raise InputError
    if re.search(emailPattern, email) == None:
        raise InputError

    # checking if email is already being used
    for i in range(len(data["users"])):
        if (data["users"][i]["email"] == email):
            raise InputError

    # looping until we reach the user with corresponding token
    # and changing their email
    for user in data['users']:
        if token == user['token']:
            user['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)
    '''

    check_token(token)

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError

    # checking if handle_str is already being used
    for i in range(len(data["users"])):
        if (data["users"][i]["handle"] == handle_str):
            raise InputError

    # looping until we reach the user with corresponding token
    # and changing their respective handle_str
    for user in data['users']:
        if token == user['token']:
            user['handle'] = handle_str

    return {
    }

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a URL of an image on the internet, crops the image within bounds 
    (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
    '''

    check_token(token)

    # grabbing file type by spliting and checking if it is valid
    try:
        file_type = img_url.rsplit('.', 1)[1].lower()
    except:
        raise InputError("Wrong file type, must be .jpg or .jpeg")

    if not file_type in ['jpg', 'jpeg']:
        raise InputError("Wrong file type, must be .jpg or .jpeg")

    if x_end < x_start or y_end < y_start:
        raise InputError("Wrong dimensions")

    # storing image in file
    file_name = f'{random_string(10)}.{file_type}'
    urllib.request.urlretrieve(img_url, file_name)

    image = Image.open(file_name)

    # error checking dimensions of image
    width, height = image.size

    if x_start > width or x_end > width or y_start > height or y_end > height:
        raise InputError("Dimensions not within range")


    cropped_image = image.crop((x_start, y_start, x_end, y_end))
    cropped_image.save(file_name) 

    # storing cropped image in global data variable as accesible url
    user = get_user_from_token(token)

    # changing global variable user image
    user['profile_img_url'] = f'{Flask_request.url_root}images/{file_name}'

    # changing user profile image in the channels they are part of
    for channel in data['channels']:
        for member in channel['all_members']:
            if user['u_id'] == member['u_id']:
                member['profile_img_url'] = f'{Flask_request.url_root}images/{file_name}'
        for member in channel['owner_members']:
            if user['u_id'] == member['u_id']:
                member['profile_img_url'] = f'{Flask_request.url_root}images/{file_name}'
    
    return {}


  