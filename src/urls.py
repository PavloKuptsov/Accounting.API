from models.url_rule import UrlRule
from resources.account_handler import AccountHandler
from resources.accounts_handler import AccountsHandler
from resources.categories_handler import CategoriesHandler
from resources.category_handler import CategoryHandler
from resources.currencies_handler import CurrenciesHandler
from resources.transaction_handler import TransactionHandler
from resources.transactions_handler import TransactionsHandler

rules = [
    UrlRule('/api/v1.0/accounts/', AccountsHandler, 'accounts'),
    UrlRule('/api/v1.0/account/<int:id>', AccountHandler, 'account'),
    UrlRule('/api/v1.0/currencies/', CurrenciesHandler, 'currencies'),
    UrlRule('/api/v1.0/categories/', CategoriesHandler, 'categories'),
    UrlRule('/api/v1.0/categories/<int:id>', CategoryHandler, 'category'),
    UrlRule('/api/v1.0/transactions/', TransactionsHandler, 'transactions'),
    UrlRule('/api/v1.0/transaction/<int:id>', TransactionHandler, 'transaction'),
]