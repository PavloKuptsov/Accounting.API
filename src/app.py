from flask import Flask, jsonify, make_response
from config import RESPONSE_NOT_FOUND
from utils.custom_json_encoder import CustomJSONEncoder
from urls import rules
from flask_restful import Api


class MyConfig(object):
    RESTFUL_JSON = {'cls': CustomJSONEncoder}


class Server(Flask):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)


app = Server(__name__)
app.config.from_object(MyConfig)
api = Api(app)
for rule in rules:
    api.add_resource(rule.view, rule.url)


@app.errorhandler(RESPONSE_NOT_FOUND)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), RESPONSE_NOT_FOUND)
