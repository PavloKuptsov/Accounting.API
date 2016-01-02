from balance import Balance
from base_test import BaseTest
from test_data import TEST_ACCOUNT, TEST_USERNAME2, TEST_PASSWORD2


class TestBalances(BaseTest):

    # def test_func_204(self):
        pass

    # def test_func_list_balances(self):
    #     self.create_user(TEST_USERNAME2, TEST_PASSWORD2)
    #     response = self.get('/api/balances/', True)
    #     self.assertEquals(response.json, TEST_ACCOUNT)
    #
    # def test_func_add_balance_to_account(self):
    #     pass
    # #
    # # def test_func_adding_duplicate_balance_fails(self):
    # #     pass
    #
    # def test_unit_account_created(self):
    #     self.create_valid_account()
    #     acc = self.repository.list_accounts()
    #     self.assertTrue(isinstance(acc, list), len(acc) > 0)
    #
    # def test_unit_account_has_balance(self):
    #     self.create_valid_account()
    #     acc = self.repository.list_accounts()
    #     bal = len(acc) > 0 and acc[0].balances
    #     self.assertTrue(isinstance(acc, list) and len(bal) > 0 and isinstance(bal[0], Balance), 'Balances are: ' + str(bal))
    #
    # def test_unit_add_account_to_user(self):
    #     self.create_other_valid_account()
    #     accounts = self.repository.list_accounts()
    #     self.assertGreater(len(accounts), 1)
    #     self.assertEqual(accounts[1].user_id, 1)
    #
    # def test_unit_add_balance_to_account(self):
    #     self.create_valid_balance()
    #     balances = self.repository.list_accounts()[0].balances
    #     self.assertTrue(len(balances) > 1 and isinstance(balances[1], Balance), 'Balances are: ' + str(balances))
