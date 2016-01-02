from models.url_rule import UrlRule
from account_handler import AccountHandler
from accounts_handler import AccountsHandler
# from resources.categories_handler import CategoriesHandler
# from resources.category_handler import CategoryHandler
# from resources.currencies_handler import CurrenciesHandler
# from resources.transaction_handler import TransactionHandler
# from resources.transactions_handler import TransactionsHandler
from signup_handler import SignupHandler

rules = [
    UrlRule('/api/signup/', SignupHandler, 'signup'),
    UrlRule('/api/accounts/', AccountsHandler, 'accounts'),
    UrlRule('/api/accounts/<int:account_id>/', AccountHandler, 'account'),
    # UrlRule('/api/v1.0/currencies/', CurrenciesHandler, 'currencies'),
    # UrlRule('/api/v1.0/categories/', CategoriesHandler, 'categories'),
    # UrlRule('/api/v1.0/categories/<int:id>', CategoryHandler, 'category'),
    # UrlRule('/api/v1.0/transactions/', TransactionsHandler, 'transactions'),
    # UrlRule('/api/v1.0/transaction/<int:id>', TransactionHandler, 'transaction'),
]