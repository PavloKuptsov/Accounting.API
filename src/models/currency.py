from sqlalchemy import Column, Integer, Unicode, String
from config import DB


class Currency(DB.Model):
    __tablename__ = 'currency'

    currency_id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    short_name = Column(String(3))
    sign = Column(Unicode(1))

    def __init__(self, currency_id, name, short_name, sign):
        self.currency_id = currency_id
        self.name = name
        self.short_name = short_name
        self.sign = sign

    @staticmethod
    def __dir__():
        return ['currency_id', 'name', 'short_name', 'sign']
