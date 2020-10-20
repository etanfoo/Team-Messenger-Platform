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

@APP.route("/channel/messages", methods = ["GET"])
def http_channel_messages():
    data = {
        'token': request.args.get('token'),
        'channel_id': request.args.get('channel_id'),
        'start': request.args.get('start')
    }
    return dumps(channel_messages(data['token'], data['channel_id'], data['start']))

@APP.route("/channel/leave", methods = ['POST'])
def http_channel_leave():
    data = request.get_json()
    return dumps(channel_leave(data['token'], data['channel_id']))

@APP.route("/channel/join", methods = ["POST"])
def http_channel_join():
    data = request.get_json()
    return dumps(channel_join(data['token'], data['channel_id']))

@APP.route("/channel/addowner", methods = ['POST'])
def http_channel_addowner():
    data = request.get_json()
    return dumps(channel_addowner(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channel/removeowner", methods = ['POST'])
def http_channel_removeowner():
    data = request.get_json()
    return dumps(channel_removeowner(data['token'], data['channel_id'], data['u_id']))




if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port

