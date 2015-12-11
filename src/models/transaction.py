from base_model import BaseModel


class Transaction(BaseModel):
    def __init__(self, transaction_id, transaction_type_id, amount, balance_id, target_balance_id, previous_balance,
                 category_id, comment, date, exchange_rate):
        self.transaction_id = transaction_id
        self.transaction_type_id = transaction_type_id
        self.amount = amount
        self.balance_id = balance_id
        self.target_balance_id = target_balance_id
        self.previous_balance = previous_balance
        self.category_id = category_id
        self.comment = comment
        self.date = date
        self.exchange_rate = exchange_rate

    @staticmethod
    def __dir__():
        return ['transaction_id', 'transaction_type_id', 'amount', 'balance_id', 'target_balance_id',
                'previous_balance', 'category_id', 'comment', 'date', 'exchange_rate']
