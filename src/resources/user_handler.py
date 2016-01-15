from flask import request, jsonify, make_response, g
from flask.ext.restful import abort

from base_handler import BaseHandler, verify_password
from config import auth


class UserHandler(BaseHandler):

    @auth.login_required
    def get(self, user_id):
        if user_id != g.user.user_id:
            abort(401, error='You have no access to another user\'s information')
        user = self.repository.user_by_id_search(user_id)
        if not user:
            return make_response(jsonify(), 204)
        return user

    @auth.login_required
    def put(self, user_id):
        if user_id != g.user.user_id:
            abort(401, error='You have no access to another user\'s information')
        old_password = request.get_json().get('old_password')
        new_password = request.get_json().get('new_password')
        if old_password is None or new_password is None:
            abort(400, error='No input parameters')
        if verify_password(g.user.username, old_password):
            self.repository.user_change_password(user_id, new_password)
            return make_response(jsonify(), 200)
        else:
            abort(400, error='Old password is wrong')

    @auth.login_required
    def delete(self, user_id):
        self.repository.user_delete(user_id)
