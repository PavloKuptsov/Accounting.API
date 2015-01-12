from models.account import Account
from models.balance import Balance
from models.category import Category
from models.currency import Currency
from models.database_operation_result import DatabaseOperationResult
from models.transaction import Transaction
from utils.db_helper import DBHelper


class Repository(object):

    def __init__(self):
        self.db = DBHelper()

    def list_accounts(self):
        accounts = self.db.list('accounts_list')
        result = accounts and [Account.create(i) for i in accounts] or []
        if result:
            for acc in result:
                acc.balances = self.get_account_balances(acc.id)
        return result

    def get_account(self, id):
        result = self.db.get('account_get', (id,))
        account = result and Account.create(result) or None
        if result:
            account.balances = self.get_account_balances(account.id)
        return account

    def get_account_balances(self, id):
        result = self.db.search('balances_search', (id,))
        balances = result and [Balance.create(i) for i in result] or []
        for balance in balances:
            balance.currency = self.get_currency(balance.currency_id)
        return balances

    def list_currencies(self):
        result = self.db.list('currencies_list')
        return result and [Currency.create(i) for i in result] or []

    def get_currency(self, id):
        result = self.db.get('currency_get', (id,))
        return result and Currency.create(result) or None

    def list_transactions(self):
        result = self.db.list('transactions_list')
        return result and [Transaction.create(i) for i in result] or []

    def list_categories(self):
        result = self.db.list('categories_list')
        return result and [Category.create(i) for i in result] or []

    def create_transaction(self, trans):
        proc_name = 'transaction_create'
        result = self.db.create(proc_name,
                                (trans.type_id,
                                 trans.amount,
                                 trans.previous_balance,
                                 trans.balance_id,
                                 trans.target_balance_id,
                                 trans.category_id,
                                 trans.comment,
                                 trans.date))
        return result and DatabaseOperationResult(True, result[proc_name])