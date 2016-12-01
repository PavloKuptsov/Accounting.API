# coding=utf-8
from decimal import Decimal

from config import DB
from models.account import Account
from models.account_type import AccountType
from models.balance import Balance
from models.category import Category
from models.category_type import CategoryType
from models.currency import Currency
from models.global_variables import TRANSACTION_TYPE_INCOME, TRANSACTION_TYPE_SPENDING, TRANSACTION_TYPE_TRANSFER
from models.transaction import Transaction
from models.transaction_type import TransactionType
from models.user import User


class Repository(object):

    def user_create(self, username, password):
        account = Account(1, u'Cash', 1, 0)
        user = User(username, password, [])
        user.hash_password(password)
        user.accounts = [account]
        DB.session.add(user)
        DB.session.commit()
        return user.user_id

    def user_search(self, username):
        return User.query.filter_by(username=username).first()

    def user_id_search(self, username):
        return self.user_search(username).user_id

    def user_by_id_search(self, user_id):
        return User.query.filter_by(user_id=user_id).first()

    def user_delete(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        DB.session.delete(user)
        DB.session.commit()

    def user_list_accounts(self, user_id):
        accounts = Account.query.filter_by(user_id=user_id).all()
        return accounts

    def account_is_a_duplicate(self, user_id, name):
        account = Account.query.filter_by(user_id=user_id, name=name).first()
        return bool(account)

    def account_create(self, type_id, name, user_id, currency_id, balance):
        user = User.query.filter(User.user_id == user_id).first()
        acc = Account(type_id, name, currency_id, balance)
        user.accounts.append(acc)
        DB.session.commit()
        return acc.account_id

    def balance_create(self, account_id, currency_id, balance):
        acc = Account.query.filter(Account.account_id == account_id).first()
        bal = Balance(currency_id, balance)
        acc.balances.append(bal)
        DB.session.commit()
        return bal.balance_id

    def balance_get(self, balance_id):
        return Balance.query.filter_by(balance_id=balance_id).first()

    def account_delete(self, account_id):
        acc = Account.query.filter_by(account_id=account_id).first()
        DB.session.delete(acc)
        DB.session.commit()

    def account_get(self, account_id):
        return Account.query.filter_by(account_id=account_id).first()

    def account_change(self, account_id, type_id, name):
        acc = self.account_get(account_id)
        acc.type_id = type_id
        acc.name = name
        DB.session.commit()

    def user_change_password(self, user_id, password):
        user = User.query.filter_by(user_id=user_id).first()
        user.hash_password(password)
        DB.session.commit()

    def account_list_balances(self, account_id):
        return Balance.query.filter_by(account_id=account_id).all()

    def categories_list(self, user_id):
        return Category.query.filter_by(user_id=user_id).all()

    def category_create(self, user_id, name, parent_category_id, type_id):
        cat = Category(user_id, name, parent_category_id, type_id)
        DB.session.add(cat)
        DB.session.commit()
        return cat.category_id

    def category_change(self, category_id, name, parent_category_id):
        category = Category.query.filter_by(category_id=category_id).first()
        category.name = name
        category.parent_category_id = parent_category_id
        DB.session.commit()

    def category_get(self, category_id):
        return Category.query.filter_by(category_id=category_id).first()

    def category_delete(self, category_id):
        category = self.category_get(category_id)
        DB.session.delete(category)
        DB.session.commit()

    def category_is_a_duplicate(self, user_id, name, parent_category_id):
        cat = Category.query.filter_by(user_id=user_id, name=name, parent_category_id=parent_category_id).first()
        return bool(cat)

    def transaction_create(self, transaction_type_id, amount, balance_id, category_id, comment, date, exchange_rate,
                           target_balance_id, child_to=None):
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
            balance.balance -= amount
            self.transaction_create(transaction_type_id=transaction_type_id,
                                    amount=Decimal(amount * exchange_rate),
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
        return trans.transaction_id

    def transaction_delete(self, transaction_id):
        trans = Transaction.query.filter_by(transaction_id=transaction_id).first()
        balance = Balance.query.filter_by(balance_id=trans.balance_id).first()

        if trans.transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance -= trans.amount
        elif trans.transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance += trans.amount
        else:
            child_trans = Transaction.query.filter_by(child_to=trans.transaction_id).first()
            target_balance = Balance.query.filter_by(balance_id=child_trans.balance_id).first()
            balance.balance += trans.amount
            target_balance.balance -= child_trans.amount
            DB.session.delete(child_trans)
        DB.session.delete(trans)
        DB.session.commit()

    def transaction_change(self, transaction_id, transaction_type_id, amount, balance_id, category_id, comment, date,
                           exchange_rate, target_balance_id):
        trans = Transaction.query.filter_by(transaction_id=transaction_id).first()
        balance = Balance.query.filter_by(balance_id=balance_id).first()

        if trans.transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance -= trans.amount
        elif trans.transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance += trans.amount
        elif trans.transaction_type_id == TRANSACTION_TYPE_TRANSFER:
            child_trans = Transaction.query.filter_by(child_to=trans.transaction_id).first()
            target_balance = Balance.query.filter_by(balance_id=child_trans.balance_id).first()
            balance.balance += trans.amount
            target_balance.balance -= child_trans.amount
            DB.session.delete(child_trans)

        trans.transaction_type_id = transaction_type_id
        trans.amount = amount
        trans.balance_id = balance_id
        trans.category_id = category_id
        trans.comment = comment
        trans.date = date
        trans.exchange_rate = exchange_rate

        if transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance += amount
        elif transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance -= amount
        elif transaction_type_id == TRANSACTION_TYPE_TRANSFER:
            balance.balance -= amount
            self.transaction_create(transaction_type_id=transaction_type_id,
                                    amount=Decimal(amount * exchange_rate),
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
        return trans.transaction_id

    def transaction_search_by_account(self, account_id):
        balance_ids = Balance.query.with_entities(Balance.balance_id).filter_by(account_id=account_id).all()
        transactions = Transaction.query.filter(Transaction.balance_id.in_(balance_ids)).all()
        return transactions

    def transactions_search_by_user_id(self, user_id):
        account_ids = Account.query.with_entities(Account.account_id).filter_by(user_id=user_id).all()
        balance_ids = Balance.query.with_entities(Balance.balance_id).filter(Balance.account_id.in_(account_ids)).all()
        transactions = Transaction.query.filter(Transaction.balance_id.in_(balance_ids)).all()
        return transactions

    def transactions_search_by_category_id(self, category_id):
        return Transaction.query.filter_by(category_id=category_id).all()


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
        # self.transaction_create(1, 100, 1, 1, u'Test income trans', datetime.now().date(), 1, None)
