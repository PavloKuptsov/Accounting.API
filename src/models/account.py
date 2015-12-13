from sqlalchemy import Integer, Column, Unicode
from sqlalchemy.orm import relationship

from config import DB
from balance import Balance


class Account(DB.Model):
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    name = Column(Unicode(100))
    owner_id = Column(Integer)
    balances = relationship(Balance)

    def __init__(self, account_id, type_id, name, owner_id, default_currency_id, balances):
        self.account_id = account_id
        self.type_id = type_id
        self.name = name
        self.owner_id = owner_id
        self.default_currency_id = default_currency_id
        self.balances = balances

    @staticmethod
    def __dir__():
        return ['account_id', 'type_id', 'name', 'owner_id', 'balances']
