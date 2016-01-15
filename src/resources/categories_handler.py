from flask import request, g, make_response, jsonify
from flask.ext.restful import abort

from base_handler import BaseHandler
from config import auth


class CategoriesHandler(BaseHandler):

    @auth.login_required
    def get(self):
        categories = self.repository.categories_list(g.user.user_id)
        if not categories:
            return make_response(jsonify(), 204)
        return categories

    @auth.login_required
    def post(self):
        user_id = g.user.user_id
        name = request.get_json().get('name')
        parent_category_id = request.get_json().get('parent_category_id')
        type_id = request.get_json().get('type_id')

        if self.repository.category_is_a_duplicate(user_id, name, parent_category_id):
            abort(400, error='Category already exists')
        category_id = self.repository.category_create(user_id, name, parent_category_id, type_id)
        return make_response(jsonify({'category_id': category_id}), 201)

    @auth.login_required
    def put(self):
        pass #TODO: Migrate transactions to other category