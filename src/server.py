import sys
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from error import InputError
from channels import channels_list, channels_listall, channels_create
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle

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
    return dumps(channels_list(new_data["token"]))

@APP.route("/channels/listall", methods = ["GET"])
def http_channels_listall():
    new_data = {
        "token": request.args.get("token")
    }
    return dumps(channels_listall(new_data["token"]))

@APP.route("/channels/create", methods = ["POST"])
def http_channels_create():
    new_data = request.get_json()
    return dumps(channels_create(new_data["token"], new_data["name"], new_data["is_public"]))





####################
# User functions
####################
@APP.route('/user/profile', methods = ['GET'])
def http_user_profile():
    data = request.args
    return jsonify(user_profile(data['token'], int(data['u_id'])))

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







if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port



