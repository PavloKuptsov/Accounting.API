# coding=utf-8

from config import DB
from models.currency import Currency


class CurrenciesRepository(object):

    @staticmethod
    def currency_create(name, short_name, sign):
        curr = Currency(name, short_name, sign)
        DB.session.add(curr)
        DB.session.commit()
        return curr.currency_id

    @staticmethod
    def currencies_list():
        return Currency.query.all()

    @staticmethod
    def currency_delete(currency_id):
        curr = Currency.query.filter_by(currency_id=currency_id).first()
        DB.session.delete(curr)
        DB.session.commit()


