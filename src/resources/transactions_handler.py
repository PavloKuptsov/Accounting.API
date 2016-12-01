from flask import request, make_response, jsonify, g

from config import auth
from resources.base_handler import BaseHandler


class TransactionsHandler(BaseHandler):

    @auth.login_required
    def get(self):
        transactions = self.repository.transactions_search_by_user_id(g.user.user_id)
        if not transactions:
            return make_response(jsonify(), 204)
        return transactions

    @auth.login_required
    def post(self):
        transaction_type_id = request.get_json().get('transaction_type_id')
        amount = request.get_json().get('amount')
        balance_id = request.get_json().get('balance_id')
        category_id = request.get_json().get('category_id')
        comment = request.get_json().get('comment')
        date = request.get_json().get('date')
        exchange_rate = request.get_json().get('exchange_rate')

        transaction_id = self.repository.transaction_create(transaction_type_id, amount, balance_id, category_id,
                                                            comment, date, exchange_rate, None)
        return make_response(jsonify({'transaction_id': transaction_id}), 201)
