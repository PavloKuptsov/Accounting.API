# coding=utf-8
from decimal import Decimal

from datetime import datetime

from account import Account
from account_type import AccountType
from balance import Balance
from category import Category
from category_type import CategoryType
from config import DB
from currency import Currency
from global_variables import TRANSACTION_TYPE_INCOME, TRANSACTION_TYPE_SPENDING, TRANSACTION_TYPE_TRANSFER
from transaction import Transaction
from transaction_type import TransactionType
from user import User


class Repository(object):

    def create_user(self, username, password):
        account = Account(1, u'Cash', 1, 0)
        user = User(username, password, [])
        user.hash_password(password)
        user.accounts = [account]
        DB.session.add(user)
        DB.session.commit()
        return user.user_id

    def search_user(self, username):
        return User.query.filter_by(username=username).first()

    def search_user_id(self, username):
        return self.search_user(username).user_id

    def search_user_by_id(self, user_id):
        return User.query.filter_by(user_id=user_id).first()

    def delete_user(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        DB.session.delete(user)
        DB.session.commit()

    def list_user_accounts(self, user_id):
        accounts = Account.query.filter_by(user_id=user_id).all()
        return accounts

    def is_account_a_duplicate(self, user_id, name):
        account = Account.query.filter_by(user_id=user_id, name=name).first()
        return bool(account)

    def add_account(self, type_id, name, user_id, currency_id, balance):
        user = User.query.filter(User.user_id == user_id).first()
        acc = Account(type_id, name, currency_id, balance)
        user.accounts.append(acc)
        DB.session.commit()
        return acc.account_id

    def add_balance(self, account_id, currency_id, balance):
        acc = Account.query.filter(Account.account_id == account_id).first()
        bal = Balance(currency_id, balance)
        acc.balances.append(bal)
        DB.session.commit()
        return bal.balance_id

    def get_balance(self, balance_id):
        return Balance.query.filter_by(balance_id=balance_id).first()

    def delete_account(self, account_id):
        acc = Account.query.filter_by(account_id=account_id).first()
        DB.session.delete(acc)
        DB.session.commit()

    def get_account(self, account_id):
        return Account.query.filter_by(account_id=account_id).first()

    def change_account(self, account_id, type_id, name):
        acc = self.get_account(account_id)
        acc.type_id = type_id
        acc.name = name
        DB.session.commit()

    def change_user_password(self, user_id, password):
        user = User.query.filter_by(user_id=user_id).first()
        user.hash_password(password)
        DB.session.commit()

    def list_account_balances(self, account_id):
        return Balance.query.filter_by(account_id=account_id).all()

    def list_categories(self, user_id):
        return Category.query.filter_by(user_id=user_id).all()

    def create_category(self, user_id, name, parent_category_id, type_id):
        cat = Category(user_id, name, parent_category_id, type_id)
        DB.session.add(cat)
        DB.session.commit()
        return cat.category_id

    def is_category_a_duplicate(self, user_id, name, parent_category_id):
        cat = Category.query.filter_by(user_id=user_id, name=name, parent_category_id=parent_category_id).first()
        return bool(cat)

    def add_transaction(self, transaction_type_id, amount, balance_id, category_id, comment, date, exchange_rate,
                        child_to, target_balance_id):
        trans = Transaction(transaction_type_id, amount, balance_id, category_id, comment, date, exchange_rate,
                            child_to)
        balance = Balance.query.filter_by(balance_id=balance_id).first()
        DB.session.add(trans)
        DB.session.flush()
        if transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance += amount
        elif transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance -= amount
        elif transaction_type_id == TRANSACTION_TYPE_TRANSFER and not child_to:
            # print('transaction_type_id: ' + str(transaction_type_id))
            # print('child_to: ' + str(child_to))
            # print('balance_id: ' + str(balance_id))
            # print('balance: ' + str(balance))
            balance.balance -= amount
            self.add_transaction(transaction_type_id=transaction_type_id,
                                 amount=Decimal(amount*exchange_rate),
                                 balance_id=target_balance_id,
                                 category_id=None,
                                 comment=None,
                                 date=None,
                                 exchange_rate=None,
                                 child_to=trans.transaction_id,
                                 target_balance_id=None)
        else:
            balance.balance += amount
        DB.session.commit()

    def create_initial_testing_data(self):
        DB.session.add(AccountType(1, u'Cash'))
        DB.session.add(AccountType(2, u'Credit'))
        DB.session.commit()
        account = Account(1, u'Cash', 3, 0)
        user = User('test_username', 'test_password', [])
        user.hash_password('test_password')
        user.accounts = [account]
        DB.session.add(user)
        DB.session.commit()
        DB.session.add(CategoryType(1, u'Income'))
        DB.session.add(CategoryType(2, u'Spending'))
        DB.session.add(TransactionType(1, u'Income'))
        DB.session.add(TransactionType(2, u'Spending'))
        DB.session.add(TransactionType(3, u'Transfer'))
        DB.session.commit()
        DB.session.add(Category(1, u'Sample income category', None, 1))
        DB.session.add(Category(1, u'Sample spending category', None, 2))
        DB.session.add(Category(1, u'Sample child spending category', 2, 2))
        DB.session.add(Currency(1, u'US dollar', 'USD', u'$'))
        DB.session.add(Currency(2, u'Euro', 'EUR', u'€'))
        DB.session.add(Currency(3, u'Ukrainian hryvna', 'UAH', u'₴'))
        DB.session.add(Currency(4, u'British pound', 'GBP', u'£'))
        DB.session.add(Currency(5, u'Russian ruble', 'RUB', u'₽'))
        DB.session.commit()
