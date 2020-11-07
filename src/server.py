'''
Importing required modules and functions to run the server
'''
import sys
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from error import InputError, AccessError
from channels import channels_list, channels_listall, channels_create
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from auth import auth_login, auth_logout, auth_register
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from other import users_all, admin_userpermission_change, search
from message import message_send, message_remove, message_edit
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
    return dumps({'data': data})


###################
# channels
###################
@APP.route("/channels/list", methods=["GET"])
def http_channels_list():
    ''' 
    Loops through the list of channels and each member in that channel,
    checking if the current user is part of that channel. If so, add
    the channel details to the authorized_channels list. 
    
    Return: a list of channels the user is part of
    '''

    new_data = {"token": request.args.get("token")}
    return jsonify(channels_list(new_data["token"]))


@APP.route("/channels/listall", methods=["GET"])
def http_channels_listall():
    ''' 
    Adds all public channels and loops through the list private 
    of channels, checking if the current user is part of that channel. If so, add
    the channel details to the authorized_channels list. 

    Return: a list of all public channels and any private channels the user is part of
    '''

    new_data = {"token": request.args.get("token")}
    return jsonify(channels_listall(new_data["token"]))


@APP.route("/channels/create", methods=["POST"])
def http_channels_create():
    ''' 
    Create a public/private channel with a given name, and add the current user’s details to “owner_members” and “all_members”
    Return: the channel_id
    '''
    new_data = request.get_json()
    return jsonify(
        channels_create(new_data["token"], new_data["name"],
                        new_data["is_public"]))


###################
# channel
###################

# data is passed through the URL for GET methods
# post put and delete does not pass the data through the URL, its rather passed as a body/packet sent to the web server


@APP.route("/channel/invite", methods=["POST"])
def http_channel_invite():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(
        channel_invite(data['token'], int(data['channel_id']), int(data['u_id'])))


@APP.route("/channel/details", methods=["GET"])
def http_channel_details():
    '''
    Grabs data from the URL
    Sends selected data from the URL to the function
    '''
    data = request.args
    return jsonify(channel_details(data['token'], int(data['channel_id'])))


@APP.route("/channel/messages", methods=["GET"])
def http_channel_messages():
    '''
    Grabs data from the URL
    Sends selected data from the URL to the function
    '''
    data = request.args
    return jsonify(
        channel_messages(data['token'], int(data['channel_id']),
                         int(data['start'])))


@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(channel_leave(data['token'], int(data['channel_id'])))


@APP.route("/channel/join", methods=["POST"])
def http_channel_join():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(channel_join(data['token'], int(data['channel_id'])))


@APP.route("/channel/addowner", methods=['POST'])
def http_channel_addowner():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(
        channel_addowner(data['token'], int(data['channel_id']), int(data['u_id'])))


@APP.route("/channel/removeowner", methods=['POST'])
def http_channel_removeowner():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(
        channel_removeowner(data['token'], int(data['channel_id']),
                            int(data['u_id'])))


###################
# auth
###################
@APP.route("/auth/login", methods=['POST'])
def http_auth_login():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(auth_login(data['email'], data['password']))


@APP.route("/auth/logout", methods=['POST'])
def http_auth_logout():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(auth_logout(data['token']))


@APP.route("/auth/register", methods=['POST'])
def http_auth_register():
    '''
    Grabs data from the server.
    Send the correct data to the functions.
    '''
    data = request.get_json()
    return jsonify(
        auth_register(data['email'], data['password'], data['name_first'],
                      data['name_last']))


####################
# User functions
####################
@APP.route('/user/profile', methods=['GET'])
def http_user_profile():
    '''
    For a valid user, returns information about their email, 
    first name, last name, and handle
    '''

    data = request.args
    return jsonify(user_profile(data['token'], int(data['u_id'])))


@APP.route('/user/profile/setname', methods=['PUT'])
def http_user_profile_setname():
    '''
    Update the authorised user's first and last name
    '''

    data = request.get_json()
    return jsonify(
        user_profile_setname(data['token'], data['name_first'],
                             data['name_last']))


@APP.route('/user/profile/setemail', methods=['PUT'])
def http_user_profile_setemail():
    '''
    Update the authorised user's email address
    '''

    data = request.get_json()
    return jsonify(user_profile_setemail(data['token'], data['email']))


@APP.route('/user/profile/sethandle', methods=['PUT'])
def http_user_profile_sethandle():
    '''
    Update the authorised user's handle (i.e. display name)
    '''

    data = request.get_json()
    return jsonify(user_profile_sethandle(data['token'], data['handle_str']))


####################
# other functions
####################
@APP.route('/users/all', methods=['GET'])
def http_users_all():
    '''
    Returns a list of all users and their associated details
    '''

    data = request.args
    return jsonify(users_all(data['token']))


@APP.route('/admin/userpermission/change', methods=['POST'])
def http_admin_userpermission_change():
    '''
    Given a User by their user ID, set their permissions to new permissions described by permission_id
    '''

    data = request.get_json()
    return jsonify(
        admin_userpermission_change(data['token'], int(data['u_id']),
                                    data['permission_id']))


@APP.route('/search', methods=['GET'])
def http_search():
    '''
    Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
    '''

    data = request.args
    return jsonify(search(data['token'], data['query_str']))


###################
# MESSAGE
###################
@APP.route('/message/send', methods=['POST'])
def http_message_send():
    ''' 
    Send a message from authorised_user to the channel specified by channel_id
    '''

    data = request.get_json()
    return jsonify(
        message_send(data['token'], int(data['channel_id']), data['message']))


@APP.route('/message/remove', methods=['DELETE'])
def http_message_remove():
    ''' 
    Given a message_id for a message, this message is removed from the channel
    '''

    data = request.get_json()
    return jsonify(message_remove(data['token'], data['message_id']))


@APP.route('/message/edit', methods=['PUT'])
def http_message_edit():
    ''' 
    Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.
    '''

    data = request.get_json()
    return jsonify(
        message_edit(data['token'], data['message_id'], data['message']))


@APP.route('/clear', methods=['DELETE'])
def http_clear():
    ''' 
    Resets the internal data of the application to it's initial state
    '''

    return jsonify(clear())


if __name__ == "__main__":
    APP.run(port=0)  # Do not edit this port
