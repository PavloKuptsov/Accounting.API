from models.url_rule import UrlRule
from views.account_handler import AccountHandler
from views.accounts_handler import AccountsHandler
from views.categories_handler import CategoriesHandler
from views.currencies_handler import CurrenciesHandler
from views.transactions_handler import TransactionsHandler

rules = []
rules.extend([
    UrlRule('/api/v1.0/accounts/', AccountsHandler, 'accounts'),
    UrlRule('/api/v1.0/account/<int:id>', AccountHandler, 'account'),
    UrlRule('/api/v1.0/currencies/', CurrenciesHandler, 'currencies'),
    UrlRule('/api/v1.0/categories/', CategoriesHandler, 'categories'),
    UrlRule('/api/v1.0/transactions/', TransactionsHandler, 'transactions'),
])