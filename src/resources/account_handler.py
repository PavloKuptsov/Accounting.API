from flask import request, jsonify
from config import auth
from resources.base_handler import BaseHandler


class AccountHandler(BaseHandler):

    @auth.login_required
    def get(self, account_id):
        account = self.repository.accounts.account_get(account_id)
        return jsonify(account)

    @auth.login_required
    def put(self, account_id):
        type_id = request.get_json().get('type_id')
        name = request.get_json().get('name')
        res = self.repository.accounts.account_change(account_id, type_id, name)
        return res

    @auth.login_required
    def delete(self, account_id):
        pass
