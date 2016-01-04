TEST_USERNAME = 'test_username'
TEST_PASSWORD = 'test_password'
TEST_USERNAME2 = 'test_username_2'
TEST_PASSWORD2 = 'test_password_2'
TEST_USERNAME3 = 'test_username_3'
TEST_PASSWORD3 = 'test_password_3'

TEST_CREDENTIALS_DICT = {'username': TEST_USERNAME, 'password': TEST_PASSWORD}
TEST_CREDENTIALS_DICT2 = {'username': TEST_USERNAME2, 'password': TEST_PASSWORD2}
TEST_CREDENTIALS_DICT3 = {'username': TEST_USERNAME3, 'password': TEST_PASSWORD3}

TEST_ACCOUNT = [{'type_id': 1,
                 'user_id': 1,
                 'account_id': 1,
                 'name': 'Cash',
                 'balances': [{'currency_id': 1,
                               'balance': 0,
                               'account_id': 1,
                               'balance_id': 1}]
                 }]

TEST_CATEGORIES_LIST = [{'category_id': 1,
                         'name': u'Sample income category',
                         'parent_category_id': None,
                         'type_id': 1},
                        {'category_id': 2,
                         'name': u'Sample spending category',
                         'parent_category_id': None,
                         'type_id': 2},
                        {'category_id': 3,
                         'name': u'Sample child spending category',
                         'parent_category_id': 2,
                         'type_id': 2}]

URL_USERS = '/api/users/'
URL_ACCOUNTS = '/api/accounts/'
URL_BALANCES = '/api/balances/'
URL_CATEGORIES = '/api/categories/'


def url_user(user_id):
    return URL_USERS + str(user_id) + '/'


def url_account(account_id):
    return URL_ACCOUNTS + str(account_id) + '/'


def url_balance(balance_id):
    return URL_BALANCES + str(balance_id) + '/'


def url_categories(category_id):
    return URL_CATEGORIES + str(category_id) + '/'
