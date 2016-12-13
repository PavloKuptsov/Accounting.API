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
    child_to = Column(Integer, default=None)
    order = Column(Integer, default=1)

    def __init__(self, transaction_type_id, amount, balance_id, category_id, comment, date, child_to):
        self.transaction_type_id = transaction_type_id
        self.amount = amount
        self.balance_id = balance_id
        self.category_id = category_id
        self.comment = comment
        self.date = date
        self.child_to = child_to

    @staticmethod
    def __dir__():
        return ['transaction_id', 'transaction_type_id', 'amount', 'balance_id', 'category_id', 'comment', 'date',
                'child_to', 'order']

    def __repr__(self):
        return '<Transaction id={}, type={}, amount={}, balance={}'.format(self.transaction_id,
                                                                           self.transaction_type_id,
                                                                           self.amount,
                                                                           self.balance_id)
