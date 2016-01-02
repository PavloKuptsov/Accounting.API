from sqlalchemy import Integer, Column, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from config import DB
from balance import Balance


class Account(DB.Model):
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    name = Column(Unicode(100))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    balances = relationship(Balance, cascade='all,delete')

    user = relationship('User', cascade='all,delete', back_populates='accounts')

    def __init__(self, type_id, name, currency_id, balance):
        self.type_id = type_id
        self.name = name
        self.balances = [Balance(currency_id, balance)]


    @staticmethod
    def __dir__():
        return ['account_id', 'type_id', 'name', 'user_id', 'balances']

    def __repr__(self):
        return 'Account %s, type_id %s, user_id %s, balances %s' % \
               (self.name, self.type_id, self.user_id, self.balances)
