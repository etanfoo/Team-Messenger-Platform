'''
Importing required modules and functions to run the server
'''
import sys
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from error import InputError, AccessError
from channels import channels_list, channels_listall, channels_create
from channel import (
    channel_invite, 
    channel_details, 
    channel_messages, 
    channel_leave, 
    channel_join, 
    channel_addowner, 
    channel_removeowner
)
from auth import auth_login, auth_logout, auth_register
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from other import clear

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

###################
# channels
###################
@APP.route("/channels/list", methods = ["GET"])
def http_channels_list():
    new_data = {
        "token": request.args.get("token")
    }
    return jsonify(channels_list(new_data["token"]))

@APP.route("/channels/listall", methods = ["GET"])
def http_channels_listall():
    new_data = {
        "token": request.args.get("token")
    }
    return jsonify(channels_listall(new_data["token"]))

@APP.route("/channels/create", methods = ["POST"])
def http_channels_create():
    new_data = request.get_json()
    return jsonify(channels_create(new_data["token"], new_data["name"], new_data["is_public"]))

###################
# channel 
###################

# data is passed through the URL for GET methods
# post put and delete does not pass the data through the URL, its rather passed as a body/packet sent to the web server

@APP.route("/channel/invite", methods = ["POST"])
def http_channel_invite():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(channel_invite(data['token'], data['channel_id'], data['u_id']))
    

@APP.route("/channel/details", methods = ["GET"])
def http_channel_details():
    '''
    Grabs data from the URL
    Sends selected data from the URL to the function
    '''
    data = {
        'token': request.args.get('token'),
        'channel_id': request.args.get('channel_id'),
    }
    return jsonify(channel_details(data['token'], data['channel_id']))

@APP.route("/channel/messages", methods = ["GET"])
def http_channel_messages():
    '''
    Grabs data from the URL
    Sends selected data from the URL to the function
    '''
    data = {
        'token': request.args.get('token'),
        'channel_id': request.args.get('channel_id'),
        'start': request.args.get('start')
    }
    return jsonify(channel_messages(data['token'], data['channel_id'], data['start']))

@APP.route("/channel/leave", methods = ['POST'])
def http_channel_leave():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(channel_leave(data['token'], data['channel_id']))

@APP.route("/channel/join", methods = ["POST"])
def http_channel_join():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(channel_join(data['token'], data['channel_id']))

@APP.route("/channel/addowner", methods = ['POST'])
def http_channel_addowner():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(channel_addowner(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channel/removeowner", methods = ['POST'])
def http_channel_removeowner():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(channel_removeowner(data['token'], data['channel_id'], data['u_id']))

###################
# auth 
###################
@APP.route("/auth/login", methods = ['POST'])
def http_auth_login():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(auth_login(data['email'], data['password']))

@APP.route("/auth/logout", methods = ['POST'])
def http_auth_logout():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(auth_logout(data['token']))
    
@APP.route("/auth/register", methods = ['POST'])
def http_auth_register():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(auth_register(data['email'], data['password'], data['name_first'], data['name_last']))

####################
# User functions
####################
@APP.route('/user/profile', methods = ['GET'])
def http_user_profile():
    data = request.args
    return jsonify(user_profile(data['token'], data['u_id']))

@APP.route('/user/profile/setname', methods = ['PUT'])
def http_user_profile_setname():
    data = request.get_json()
    return jsonify(user_profile_setname(data['token'], data['name_first'], data['name_last']))


@APP.route('/user/profile/setemail', methods = ['PUT'])
def http_user_profile_setemail():
    data = request.get_json()
    return jsonify(user_profile_setemail(data['token'], data['email']))

@APP.route('/user/profile/sethandle', methods = ['PUT'])
def http_user_profile_sethandle():
    data = request.get_json()
    return jsonify(user_profile_sethandle(data['token'], data['handle_str']))

####################
# Clear function
####################
@APP.route('/clear', methods = ['DELETE'])
def http_clear():
    clear()
    return jsonify({})


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port



