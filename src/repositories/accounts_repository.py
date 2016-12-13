# coding=utf-8

from config import DB
from models.account import Account
from models.balance import Balance
from models.user import User


class AccountsRepository(object):

    @staticmethod
    def list_accounts(user_id):
        accounts = Account.query.filter_by(user_id=user_id).all()
        return accounts

    @staticmethod
    def account_is_a_duplicate(user_id, name):
        account = Account.query.filter_by(user_id=user_id, name=name).first()
        return bool(account)

    @staticmethod
    def account_create(type_id, name, user_id, currency_id, balance):
        user = User.query.filter(User.user_id == user_id).first()
        acc = Account(type_id, name, currency_id, balance)
        user.accounts.append(acc)
        DB.session.commit()
        return acc.account_id

    @staticmethod
    def account_delete(account_id):
        acc = Account.query.filter_by(account_id=account_id).first()
        DB.session.delete(acc)
        DB.session.commit()

    @staticmethod
    def account_get(account_id):
        return Account.query.filter_by(account_id=account_id).first()

    @staticmethod
    def account_change(account_id, type_id, name):
        acc = AccountsRepository.account_get(account_id)
        acc.type_id = type_id
        acc.name = name
        DB.session.commit()

    @staticmethod
    def account_list_balances(account_id):
        return Balance.query.filter_by(account_id=account_id).all()
