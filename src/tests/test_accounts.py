from balance import Balance
from base_test import BaseTest
from test_data import TEST_ACCOUNT, TEST_USERNAME2, TEST_PASSWORD2


class TestAccounts(BaseTest):

    def test_func_401(self):
        response = self.get('/api/accounts/', False)
        self.assert401(response)
        self.assertTrue('WWW-Authenticate' in response.headers)
        self.assertTrue('Basic' in response.headers['WWW-Authenticate'])

    def test_func_204(self):
        self.repository.delete_account(1)
        response = self.get('/api/accounts/', True)
        self.assert_status(response, 204)

    def test_func_add_account(self):
        response = self.post('/api/accounts/', dict(type_id=1, name=u'CC', currency_id=1, balance=0), True)
        self.assert_status(response, 201)

    def test_func_auth_enter(self):
        response = self.get('/api/accounts/', True)
        self.assert200(response)

    def test_func_list_accounts(self):
        self.create_user(TEST_USERNAME2, TEST_PASSWORD2)
        response = self.get('/api/accounts/', True)
        self.assertEquals(response.json, TEST_ACCOUNT)

    def test_func_adding_duplicate_account_fails(self):
        response = self.post('/api/accounts/', dict(type_id=1, name=u'Cash', currency_id=1, balance=0), True)
        self.assert400(response, message='Account already exists')

    def test_func_rename_account(self):
        response = self.put('/api/accounts/1/', dict(type_id=2, name=u'CC'), True)
        print(response.data)
        self.assert200(response)
        acc = self.repository.list_user_accounts(1)[0]
        self.assertEquals(acc.type_id, 2)
        self.assertEquals(acc.name, u'CC')

    # def test_func_add_balance_to_account(self):
    #     pass
    #
    # def test_func_adding_duplicate_balance_fails(self):
    #     pass

    def test_unit_account_created(self):
        self.create_valid_account()
        acc = self.repository.list_user_accounts(1)
        self.assertTrue(isinstance(acc, list), len(acc) > 0)

    def test_unit_account_has_balance(self):
        self.create_valid_account()
        acc = self.repository.list_user_accounts(1)
        bal = len(acc) > 0 and acc[0].balances
        self.assertTrue(isinstance(acc, list) and len(bal) > 0 and isinstance(bal[0], Balance), 'Balances are: ' + str(bal))

    def test_unit_add_account_to_user(self):
        self.create_other_valid_account()
        accounts = self.repository.list_user_accounts(1)
        self.assertGreater(len(accounts), 1)
        self.assertEqual(accounts[1].user_id, 1)

    def test_unit_rename_account(self):
        self.repository.change_account(1, 2, u'CC')
        acc = self.repository.list_user_accounts(1)[0]
        self.assertEquals(acc.type_id, 2)
        self.assertEquals(acc.name, u'CC')
