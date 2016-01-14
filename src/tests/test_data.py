TEST_USERNAME = 'test_username'
TEST_PASSWORD = 'test_password'
TEST_USERNAME2 = 'test_username_2'
TEST_PASSWORD2 = 'test_password_2'
TEST_USERNAME3 = 'test_username_3'
TEST_PASSWORD3 = 'test_password_3'

TEST_CREDENTIALS_DICT = {'username': TEST_USERNAME, 'password': TEST_PASSWORD}
TEST_CREDENTIALS_DICT2 = {'username': TEST_USERNAME2, 'password': TEST_PASSWORD2}
TEST_CREDENTIALS_DICT3 = {'username': TEST_USERNAME3, 'password': TEST_PASSWORD3}

URL_USERS = '/api/users/'
URL_ACCOUNTS = '/api/accounts/'
URL_BALANCES = '/api/balances/'
URL_CATEGORIES = '/api/categories/'
URL_TRANSACTIONS = '/api/transactions/'


def url_user(user_id):
    return URL_USERS + str(user_id) + '/'


def url_account(account_id):
    return URL_ACCOUNTS + str(account_id) + '/'


def url_balance(balance_id):
    return URL_BALANCES + str(balance_id) + '/'


def url_category(category_id):
    return URL_CATEGORIES + str(category_id) + '/'


def url_transaction(transaction_id):
    return URL_TRANSACTIONS + str(transaction_id) + '/'
