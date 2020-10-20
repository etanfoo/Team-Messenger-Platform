import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner


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
# channel 
###################

# data is passed through the URL for GET methods
# post put and delete does not pass the data through the URL, its rather passed as a body/packet sent to the web server

@APP.route("/channel/invite", methods = ["POST"])
def http_channel_invite():
    data = request.get_json()
    return dumps(channel_invite(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channel/details", methods = ["GET"])
def http_channel_details():
    data = {
        'token': request.args.get('token'),
        'channel_id': request.args.get('channel_id'),
    }
    return dumps(channel_details(data['token'], data['channel_id']))



@APP.route("/channels/list", methods = ["GET"])
def channels_list():
    new_data = request.get_json()
    return dumps(channels_list(new_data["token"]))

@APP.route("/channels/listall", methods = ["GET"])
def channels_listall():
    new_data = request.get_json()
    return dumps(channels_listall(new_data["token"]))

@APP.route("/channels/create", methods = ["POST"])
def channels_create():
    new_data = request.get_json()
    return dumps(channels_create(new_data["token"], new_data["name"], new_data["is_public"]))









if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port

