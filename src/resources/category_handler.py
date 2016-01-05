from flask import request, jsonify
from flask.ext.restful import abort

from base_handler import BaseHandler
from config import auth


class CategoryHandler(BaseHandler):

    @auth.login_required
    def get(self, category_id):
        category = self.repository.category_get(category_id)
        return jsonify(category)

    @auth.login_required
    def put(self, category_id):
        parent_category_id = request.get_json().get('parent_category_id')
        name = request.get_json().get('name')

        parent_category = self.repository.category_get(parent_category_id)
        category = self.repository.category_get(category_id)
        if category.type_id != parent_category.type_id:
            abort(400, error='You cannot change type of category')
        result = self.repository.category_change(category_id, name, parent_category_id)
        return result

    @auth.login_required
    def delete(self, category_id):
        transactions = self.repository.transactions_search_by_category_id(category_id)
        if transactions:
            abort(400, error='Cannot delete category which has transactions')
        result = self.repository.category_delete(category_id)
        return result
