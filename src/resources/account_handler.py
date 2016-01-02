from flask import request, jsonify

from base_handler import BaseHandler
from config import auth


class AccountHandler(BaseHandler):

    @auth.login_required
    def get(self, account_id):
        account = self.repository.get_account(account_id)
        return jsonify(account)

    @auth.login_required
    def put(self, account_id):
        type_id = request.get_json().get('type_id')
        name = request.get_json().get('name')
        res = self.repository.change_account(account_id, type_id, name)
        return res
