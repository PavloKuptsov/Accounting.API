from base_test import BaseTest
from test_data import URL_BALANCES


class TestBalances(BaseTest):

    def test_func_add_balance_to_account(self):
        response = self.post(URL_BALANCES, dict(account_id=1, currency_id=2, balance=0), True)
        self.assert_status(response, 201)

    def test_func_adding_duplicate_balance_fails(self):
        response = self.post(URL_BALANCES, dict(account_id=1, currency_id=1, balance=0), True)
        self.assert400(response)
