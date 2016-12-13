# coding=utf-8

from config import DB
from models.account import Account
from models.balance import Balance


class BalancesRepository(object):

    @staticmethod
    def balance_create(account_id, currency_id, balance):
        acc = Account.query.filter(Account.account_id == account_id).first()
        bal = Balance(currency_id, balance)
        acc.balances.append(bal)
        DB.session.commit()
        return bal.balance_id

    @staticmethod
    def balance_get(balance_id):
        return Balance.query.filter_by(balance_id=balance_id).first()

    @staticmethod
    def list_balances_by_account(account_id):
        return Balance.query.filter_by(account_id=account_id).all()

