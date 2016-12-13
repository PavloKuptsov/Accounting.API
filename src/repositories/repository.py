# coding=utf-8

from config import DB
from models.account_type import AccountType
from models.category_type import CategoryType
from models.currency import Currency
from models.transaction_type import TransactionType
from repositories.accounts_repository import AccountsRepository
from repositories.balances_repository import BalancesRepository
from repositories.categories_repository import CategoriesRepository
from repositories.currencies_repository import CurrenciesRepository
from repositories.transactions_repository import TransactionsRepository
from repositories.users_repository import UsersRepository


class Repository(object):

    @property
    def users(self):
        return UsersRepository

    @property
    def accounts(self):
        return AccountsRepository

    @property
    def balances(self):
        return BalancesRepository

    @property
    def categories(self):
        return CategoriesRepository

    @property
    def transactions(self):
        return TransactionsRepository

    @property
    def currencies(self):
        return CurrenciesRepository

    def create_initial_data(self):
        DB.session.add(AccountType(1, u'Cash'))
        DB.session.add(AccountType(2, u'Credit'))
        DB.session.add(CategoryType(1, u'Income'))
        DB.session.add(CategoryType(2, u'Spending'))
        DB.session.add(TransactionType(1, u'Income'))
        DB.session.add(TransactionType(2, u'Spending'))
        DB.session.add(TransactionType(3, u'Transfer'))
        DB.session.commit()
        self.currencies.currency_create(u'US dollar', 'USD', u'$')
        self.currencies.currency_create(u'Euro', 'EUR', u'€')
        self.currencies.currency_create(u'Ukrainian hryvna', 'UAH', u'₴')
        self.currencies.currency_create(u'British pound', 'GBP', u'£')
        self.currencies.currency_create(u'Russian ruble', 'RUB', u'₽')

    def create_initial_testing_data(self):
        self.create_initial_data()
        self.users.user_create('test_username', 'test_password')
        self.categories.category_create(1, u'Sample income category', None, 1)
        self.categories.category_create(1, u'Sample spending category', None, 2)
        self.categories.category_create(1, u'Sample child spending category', 2, 2)
