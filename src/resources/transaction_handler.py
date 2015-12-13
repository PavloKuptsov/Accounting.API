from flask import request
from base_handler import BaseHandler
from models.transaction import Transaction


class TransactionHandler(BaseHandler):
    def delete(self, id):
        result = self.repository.delete_transaction(id)
        return self.json_response(result)