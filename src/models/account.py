from sqlalchemy import Integer, Column, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from config import DB
from models.balance import Balance


class Account(DB.Model):
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('account_type.type_id'))
    name = Column(Unicode(100))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    balances = relationship(Balance, cascade='all, delete-orphan', backref='account')

    def __init__(self, type_id, name, currency_id, balance):
        self.type_id = type_id
        self.name = name
        self.balances = [Balance(currency_id, balance)]

    @staticmethod
    def __dir__():
        return ['account_id', 'type_id', 'name', 'user_id', 'balances']

    def __repr__(self):
        return '<Account account_id = %s,\n name = %s \n type_id = %s, \n user_id = %s, \n balances = %s>\n' % \
               (self.account_id, self.name, self.type_id, self.user_id, self.balances)
