from base_test import BaseTest
from test_data import URL_TRANSACTIONS, url_transaction

TEST_TRANSACTION = [{'comment': u'Test income trans',
                     'child_to': None,
                     'exchange_rate': 1,
                     'amount': 100,
                     'balance_id': 1,
                     'date': u'2016-01-14',
                     'transaction_type_id': 1,
                     'category_id': 1,
                     'order': 1,
                     'transaction_id': 1}]


class TestTransactions(BaseTest):

    def test_no_transactions(self):
        response = self.get(URL_TRANSACTIONS)
        self.assert_status(response, 204)

    def test_func_get_transactions(self):
        self.repository.transaction_create(1, 100, 1, 1, u'Test income trans', self.get_today(), 1, None)
        response = self.get(URL_TRANSACTIONS)
        self.assert200(response)
        self.assertEquals(response.json, TEST_TRANSACTION)

    def test_func_add_transaction(self):
        response = self.post(URL_TRANSACTIONS, dict(transaction_type_id=1,
                                                    amount=100,
                                                    balance_id=1,
                                                    category_id=1,
                                                    comment=u'CC',
                                                    date=self.get_today().isoformat(),
                                                    exchange_rate=1,
                                                    target_balance_id=''))
        self.assert_status(response, 201)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, 100)

    def test_func_delete_transaction(self):
        self.repository.transaction_create(1, 100, 1, 1, u'Test income trans', self.get_today(), 1, None)
        response = self.delete(url_transaction(1))
        self.assert200(response)
        response = self.get(URL_TRANSACTIONS)
        self.assert_status(response, 204)

    def test_func_change_transaction(self):
        self.repository.transaction_create(1, 100, 1, 1, u'Test income trans', self.get_today(), 1, None)
        response = self.put(url_transaction(1), dict(transaction_type_id=1,
                                                     amount=30,
                                                     balance_id=1,
                                                     category_id=1,
                                                     comment=u'CC',
                                                     date=self.get_today().isoformat(),
                                                     exchange_rate=1,
                                                     target_balance_id=''))
        self.assert200(response)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, 30)

    def test_unit_add_income_transaction(self):
        self.repository.transaction_create(1, 100, 1, 1, u'Test income trans', self.get_today(), 1, None)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, 100)

    def test_unit_add_spending_transaction(self):
        self.repository.transaction_create(2, 75, 1, 2, u'Test spending trans', self.get_today(), 1, None)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, -75)

    def test_unit_transfer_with_same_currency(self):
        self.repository.account_create(1, u'CC', 1, 3, 100)
        self.repository.transaction_create(3, 75, 2, None, u'Test transfer', self.get_today(), 1, 1)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 25)

    def test_unit_transfer_with_different_currencies(self):
        self.repository.account_create(1, u'CC', 1, 1, 100)
        self.repository.transaction_create(3, 3, 2, None, u'Test transfer 2', self.get_today(), 25, 1)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 97)

    def test_unit_transfer_with_different_currencies_2(self):
        self.repository.account_create(1, u'CC', 1, 5, 100)
        self.repository.transaction_create(3, 50, 2, None, u'Test transfer 2', self.get_today(), 0.33, 1)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 16.5)
        self.assertEqual(bal2.balance, 50)

    def test_unit_change_income_transaction_sum(self):
        self.repository.transaction_create(1, 50, 1, 2, u'', self.get_today(), 1, None)
        self.repository.transaction_change(1, 1, 40, 1, 2, u'', self.get_today(), 1, None)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, 40)

    def test_unit_change_spending_transaction_sum(self):
        self.repository.transaction_create(2, 50, 1, 2, u'', self.get_today(), 1, None)
        self.repository.transaction_change(1, 2, 40, 1, 2, u'', self.get_today(), 1, None)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, -40)

    def test_unit_change_transfer_transaction_sum(self):
        self.repository.account_create(1, u'CC', 1, 3, 100)
        self.repository.transaction_create(3, 50, 2, None, u'', self.get_today(), 1, 1)
        self.repository.transaction_change(1, 3, 40, 2, None, u'', self.get_today(), 1, 1)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 40)
        self.assertEqual(bal2.balance, 60)

    def test_unit_delete_income_transaction(self):
        id = self.repository.transaction_create(1, 50, 1, 2, u'', self.get_today(), 1, None)
        self.repository.transaction_delete(id)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, 0)

    def test_unit_delete_spending_transaction(self):
        id = self.repository.transaction_create(2, 50, 1, 2, u'', self.get_today(), 1, None)
        self.repository.transaction_delete(id)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, 0)

    def test_unit_delete_transfer_transaction(self):
        self.repository.account_create(1, u'CC', 1, 5, 100)
        id = self.repository.transaction_create(3, 50, 2, None, u'', self.get_today(), 1, 1)
        self.repository.transaction_delete(id)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 0)
        self.assertEqual(bal2.balance, 100)


