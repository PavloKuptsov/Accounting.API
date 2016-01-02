from flask import g, request, make_response, jsonify
from flask.ext.restful import abort

from base_handler import BaseHandler
from config import auth


class AccountsHandler(BaseHandler):

    @auth.login_required
    def get(self):
        accounts = self.repository.list_user_accounts(g.user.user_id)
        return accounts or 204

    @auth.login_required
    def post(self):
        type_id = request.get_json().get('type_id')
        name = request.get_json().get('name')
        currency_id = request.get_json().get('currency_id')
        balance = request.get_json().get('balance')

        for account in self.repository.list_user_accounts(g.user.user_id):
            if account.name == name:
                abort(400, error='Account already exists')
        account_id = self.repository.add_account(type_id, name, g.user.user_id, currency_id, balance)
        return make_response(jsonify({'account_name': name, 'account_id': account_id}), 201)
