from flask import request, jsonify, make_response
from flask.ext.restful import abort

from base_handler import BaseHandler
from user import User


class UsersHandler(BaseHandler):

    def post(self):
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        if username is None or password is None:
            abort(400, error='No input parameters')
        if User.query.filter_by(username=username).first() is not None:
            abort(400, error='User already exists')
        user_id = self.repository.create_user(username, password)
        return make_response(jsonify({'username': username, 'user_id': user_id}), 201)
