from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from config import DB


class Balance(DB.Model):
    __tablename__ = 'balance'
    balance_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    currency_id = Column(Integer)
    balance = Column(Numeric(precision=2))

    account = relationship("Account", back_populates="balances")

    def __init__(self, balance_id, account_id, currency_id, balance, currency):
        self.balance_id = balance_id
        self.account_id = account_id
        self.currency_id = currency_id
        self.balance = balance
        self.currency = currency

    @staticmethod
    def __dir__():
        return ['balance_id', 'account_id', 'currency_id', 'balance']
