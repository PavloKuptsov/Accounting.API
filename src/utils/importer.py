import sys

from datetime import datetime
from decimal import Decimal

from models.global_variables import TRANSACTION_TYPE_TRANSFER, TRANSACTION_TYPE_INCOME, CATEGORY_TYPE_INCOME, \
    CATEGORY_TYPE_SPENDING, TRANSACTION_TYPE_SPENDING


class Importer(object):

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, repository, user_id):
        self.repository = repository
        self.user_id = user_id
        self.transactions = []
        self.transactions_parsed = []
        self.accounts_list = self.get_accounts()
        self.categories_list = self.get_categories()
        self.currencies_list = self.get_currencies()
        self.last_transaction_id = 0
        self.last_balance_id = 0
        self.last_amount = 0

    def parse(self, filename):
        with open(filename, 'r', encoding='utf8') as file:
            for line in file:
                trans_list = line.strip().split(';')
                if 'date' in trans_list[0]:
                    continue
                self.prepare(trans_list)

    def prepare(self, trans_list):
        date = trans_list[0]
        account = trans_list[1]
        category = trans_list[2]
        amount = trans_list[3]
        currency = trans_list[4]
        comment = trans_list[5]
        new_account = trans_list[6]

        child_to = new_account and ('-' not in amount)
        date = self.prepare_date(date)
        balance = self.prepare_account(account, currency)
        if category:
            category, category_type = self.prepare_category(category, amount)
        else:
            category = None
            category_type = None
        amount, transaction_type = self.prepare_amount(amount, new_account, category_type, child_to)

        if not child_to:
            self.last_balance_id = balance
            self.last_amount = amount
            self.last_transaction_id = self.repository.transactions.transaction_create(transaction_type_id=transaction_type,
                                                                                       amount=amount,
                                                                                       balance_id=balance,
                                                                                       category_id=category,
                                                                                       comment=comment,
                                                                                       date=date,
                                                                                       target_balance_id=balance,
                                                                                       target_amount=amount)
        else:
            self.repository.transactions.transaction_change(transaction_id=self.last_transaction_id,
                                                            transaction_type_id=transaction_type,
                                                            amount=self.last_amount,
                                                            balance_id=self.last_balance_id,
                                                            category_id=category,
                                                            comment=comment,
                                                            date=date,
                                                            target_balance_id=balance,
                                                            target_amount=amount)
        return

    def prepare_date(self, date):
        return datetime.strptime(date, self.DATE_FORMAT).date()

    def prepare_account(self, account_name, currency_name):
        currency_id = self.prepare_currency(currency_name)
        account = [item for item in self.accounts_list if item.name == account_name]
        if account:
            account_id = account[0].account_id
            balance = [item for item in account[0].balances if item.currency_id == currency_id]
            if balance:
                balance_id = balance[0].balance_id
            else:
                balance_id = self.repository.balances.balance_create(account_id, currency_id, 0)
        else:
            account_id = self.repository.accounts.account_create(1, account_name, self.user_id, currency_id, 0)
            balance_id = self.repository.balances.list_balances_by_account(account_id)[0].balance_id
        self.accounts_list = self.get_accounts()
        return balance_id

    def prepare_category(self, category_name, amount):
        category_id = None
        category_type_id = None
        categories = category_name.split('\\')
        for cat_name in categories:
            category = [item for item in self.categories_list if item.name == cat_name]
            if category:
                category_id = category[0].category_id
                category_type_id = category[0].type_id
            else:
                category_type_id = CATEGORY_TYPE_SPENDING if '-' in amount else CATEGORY_TYPE_INCOME
                category_id = self.repository.categories.category_create(self.user_id,
                                                                         cat_name,
                                                                         category_id,
                                                                         category_type_id)
            self.categories_list = self.get_categories()
        return category_id, category_type_id

    def prepare_amount(self, amount, new_account, category_type_id, child_to):
        if ',' in amount:
            amount = amount.replace(',', '.')
        amount = Decimal(amount)
        if new_account:
            transaction_type = TRANSACTION_TYPE_TRANSFER
            if not child_to:
                amount = -amount
        elif category_type_id == CATEGORY_TYPE_INCOME:
            transaction_type = TRANSACTION_TYPE_INCOME
        else:
            transaction_type = TRANSACTION_TYPE_SPENDING
            amount = -amount
        return amount, transaction_type

    def prepare_currency(self, currency):
        curr = [item for item in self.currencies_list if item.short_name == currency]
        if curr:
            currency_id = curr[0].currency_id
        else:
            currency_id = self.repository.currencies.currency_create(currency, currency, currency)
        self.currencies_list = self.get_currencies()
        return currency_id

    def get_accounts(self):
        return self.repository.accounts.list_accounts(self.user_id)

    def get_categories(self):
        return self.repository.categories.categories_list(self.user_id)

    def get_currencies(self):
        return self.repository.currencies.currencies_list()
