from flask import request, make_response, jsonify

from base_handler import BaseHandler
from config import auth


class TransactionHandler(BaseHandler):

    @auth.login_required
    def delete(self, transaction_id):
        self.repository.transaction_delete(transaction_id)
        return make_response(jsonify({}), 200)

    @auth.login_required
    def put(self, transaction_id):
        transaction_type_id = request.get_json().get('transaction_type_id')
        amount = request.get_json().get('amount')
        balance_id = request.get_json().get('balance_id')
        category_id = request.get_json().get('category_id')
        comment = request.get_json().get('comment')
        date = request.get_json().get('date')
        exchange_rate = request.get_json().get('exchange_rate')

        transaction_id = self.repository.transaction_change(transaction_id, transaction_type_id, amount, balance_id,
                                                            category_id, comment, date, exchange_rate, None)
        return make_response(jsonify({'transaction_id': transaction_id}), 200)
