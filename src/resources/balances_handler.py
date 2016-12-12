from flask import request, make_response, jsonify
from flask_restful import abort

from resources.base_handler import BaseHandler
from config import auth


class BalancesHandler(BaseHandler):

    @auth.login_required
    def post(self):
        account_id = request.get_json().get('account_id')
        currency_id = request.get_json().get('currency_id')
        balance = request.get_json().get('balance')

        for bal in self.repository.balances.list_balances_by_account(account_id):
            if bal.currency_id == currency_id:
                abort(400, error='Account already has this currency')
        balance_id = self.repository.balances.balance_create(account_id, currency_id, balance)
        return make_response(jsonify({'balance_id': balance_id}), 201)
