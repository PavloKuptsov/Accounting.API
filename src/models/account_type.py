from sqlalchemy import Column, Integer, Unicode
from config import DB


class AccountType(DB.Model):
    __tablename__ = 'account_type'
    type_id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))

    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    @staticmethod
    def __dir__():
        return ['type_id', 'name']
