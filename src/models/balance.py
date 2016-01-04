from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from config import DB


class Balance(DB.Model):
    __tablename__ = 'balance'
    balance_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    currency_id = Column(Integer)
    balance = Column(Numeric(scale=2))

    def __init__(self, currency_id, balance):
        self.currency_id = currency_id
        self.balance = balance

    @staticmethod
    def __dir__():
        return ['balance_id', 'account_id', 'currency_id', 'balance']

    def __repr__(self):
        return '<Balance balance_id = %s, currency_id = %s, balance = %s>' % (self.balance_id, self.currency_id, self.balance)
