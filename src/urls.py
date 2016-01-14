from balance_handler import BalanceHandler
from balances_handler import BalancesHandler
from models.url_rule import UrlRule
from account_handler import AccountHandler
from accounts_handler import AccountsHandler
from categories_handler import CategoriesHandler
from category_handler import CategoryHandler
from transaction_handler import TransactionHandler
from transactions_handler import TransactionsHandler
from user_handler import UserHandler
from users_handler import UsersHandler

rules = [
    UrlRule('/api/users/', UsersHandler, 'users'),
    UrlRule('/api/users/<int:user_id>/', UserHandler, 'user'),
    UrlRule('/api/accounts/', AccountsHandler, 'accounts'),
    UrlRule('/api/accounts/<int:account_id>/', AccountHandler, 'account'),
    UrlRule('/api/balances/', BalancesHandler, 'balances'),
    UrlRule('/api/balances/<int:balance_id>/', BalanceHandler, 'balance'),
    UrlRule('/api/categories/', CategoriesHandler, 'categories'),
    UrlRule('/api/categories/<int:category_id>/', CategoryHandler, 'category'),
    UrlRule('/api/transactions/', TransactionsHandler, 'transactions'),
    UrlRule('/api/transactions/<int:transaction_id>/', TransactionHandler, 'transaction'),
]