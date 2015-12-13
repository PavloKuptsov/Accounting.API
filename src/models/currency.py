from sqlalchemy import Column, Integer, Unicode

from config import DB


class Currency(DB.Model):
    __tablename__ = 'currency'

    currency_id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    short_name = Column(Unicode(3))

    def __init__(self, currency_id, name, short_name):
        self.currency_id = currency_id
        self.name = name
        self.short_name = short_name

    @staticmethod
    def __dir__():
        return ['currency_id', 'name', 'short_name']
