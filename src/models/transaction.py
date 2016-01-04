from sqlalchemy import Column, Integer, Numeric, Unicode, Date, ForeignKey
from config import DB


class Transaction(DB.Model):
    __tablename__ = 'transaction'

    transaction_id = Column(Integer, primary_key=True)
    transaction_type_id = Column(Integer, ForeignKey('transaction_type.type_id'))
    amount = Column(Numeric(scale=2))
    balance_id = Column(Integer, ForeignKey('balance.balance_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    comment = Column(Unicode(255))
    date = Column(Date)
    exchange_rate = Column(Numeric(scale=6), default=1)
    child_to = Column(Integer, default=None)

    def __init__(self, transaction_type_id, amount, balance_id, category_id, comment, date, exchange_rate, child_to):
        self.transaction_type_id = transaction_type_id
        self.amount = amount
        self.balance_id = balance_id
        self.category_id = category_id
        self.comment = comment
        self.date = date
        self.exchange_rate = exchange_rate
        self.child_to = child_to

    @staticmethod
    def __dir__():
        return ['transaction_id', 'transaction_type_id', 'amount', 'balance_id', 'target_balance_id',
                'previous_balance', 'category_id', 'comment', 'date', 'exchange_rate', 'child_to']
