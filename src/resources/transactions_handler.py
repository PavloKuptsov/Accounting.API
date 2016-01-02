# from flask import request
# from base_handler import BaseHandler
# from models.transaction import Transaction
#
#
# class TransactionsHandler(BaseHandler):
#     def get(self):
#         transactions = self.repository.list_transactions()
#         return self.json_response(transactions)
#
#     def post(self):
#         data = request.form
#         transaction = Transaction.create(data)
#         result = self.repository.create_transaction(transaction)
#         return self.json_response(result)
