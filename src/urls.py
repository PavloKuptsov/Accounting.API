from balance_handler import BalanceHandler
from balances_handler import BalancesHandler
from models.url_rule import UrlRule
from account_handler import AccountHandler
from accounts_handler import AccountsHandler
from resources.categories_handler import CategoriesHandler
from resources.category_handler import CategoryHandler
# from resources.currencies_handler import CurrenciesHandler
# from resources.transaction_handler import TransactionHandler
# from resources.transactions_handler import TransactionsHandler
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
    # UrlRule('/api/v1.0/currencies/', CurrenciesHandler, 'currencies'),
    # UrlRule('/api/v1.0/transactions/', TransactionsHandler, 'transactions'),
    # UrlRule('/api/v1.0/transaction/<int:id>', TransactionHandler, 'transaction'),
]