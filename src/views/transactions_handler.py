from base_handler import BaseHandler


class TransactionsHandler(BaseHandler):
    def get(self):
        transactions = self.repository.list_transactions()
        return self.json_response(transactions)
