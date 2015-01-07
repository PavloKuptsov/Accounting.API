#!../../env/bin/python
from flask import Flask, jsonify, make_response
from config import RESPONSE_NOT_FOUND
from utils.custom_json_encoder import CustomJSONEncoder
from urls import rules

class Server(Flask):

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)


app = Server(__name__)
app.json_encoder = CustomJSONEncoder
for rule in rules:
    app.add_url_rule(rule.url, view_func=rule.view().as_view(rule.name))


@app.errorhandler(RESPONSE_NOT_FOUND)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), RESPONSE_NOT_FOUND)