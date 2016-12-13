from datetime import datetime
from decimal import Decimal


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

    def parse(self, filename):
        with open(filename, 'r', encoding='utf8') as file:
            for line in file:
                trans_list = line.strip().split(';')
                if trans_list[0] == 'date':
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

        date = self.prepare_date(date)
        balance = self.prepare_account(account, currency)
        category = category and self.prepare_category(category, amount) or ''
        amount, transaction_type = self.prepare_amount(amount, new_account)
        # new_account = self.prepare_account(new_account, currency)
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
        categories = category_name.split('\\')
        for cat_name in categories:
            category = [item for item in self.categories_list if item.name == cat_name]
            if category:
                category_id = category[0].category_id
            else:
                category_type_id = 2 if '-' in amount else 1
                category_id = self.repository.categories.category_create(self.user_id,
                                                                         cat_name,
                                                                         category_id,
                                                                         category_type_id)
            self.categories_list = self.get_categories()
        return category_id

    def prepare_amount(self, amount, new_account):
        if ',' in amount:
            amount = amount.replace(',', '.')
        amount = Decimal(amount)
        if new_account:
            transaction_type = 3
        elif amount > 0:
            transaction_type = 2
        else:
            transaction_type = 1
        amount = abs(amount)
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
