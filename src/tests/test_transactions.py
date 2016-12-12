from tests.base_test import BaseTest
from tests.test_data import URL_TRANSACTIONS, url_transaction

TEST_TRANSACTION = [{'comment': u'Test income trans',
                     'child_to': None,
                     'amount': '100',
                     'balance_id': 1,
                     'date': BaseTest.get_today().isoformat(),
                     'transaction_type_id': 1,
                     'category_id': 1,
                     'order': 1,
                     'transaction_id': 1}]


class TestTransactions(BaseTest):

    def test_no_transactions(self):
        response = self.get(URL_TRANSACTIONS)
        self.assert_status(response, 204)

    def test_func_get_transactions(self):
        self.repository.transactions.transaction_create(transaction_type_id=1,
                                                        amount=100,
                                                        balance_id=1,
                                                        category_id=1,
                                                        comment=u'Test income trans',
                                                        date=self.get_today())
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
                                                    target_balance_id=''))
        self.assert_status(response, 201)
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, 100)

    def test_func_delete_transaction(self):
        self.repository.transactions.transaction_create(transaction_type_id=1,
                                                        amount=100,
                                                        balance_id=1,
                                                        category_id=1,
                                                        comment=u'Test income trans',
                                                        date=self.get_today())
        response = self.delete(url_transaction(1))
        self.assert200(response)
        response = self.get(URL_TRANSACTIONS)
        self.assert_status(response, 204)

    def test_func_change_transaction(self):
        self.repository.transactions.transaction_create(transaction_type_id=1,
                                                        amount=100,
                                                        balance_id=1,
                                                        category_id=1,
                                                        comment=u'Test income trans',
                                                        date=self.get_today())
        response = self.put(url_transaction(1), dict(transaction_type_id=1,
                                                     amount=30,
                                                     balance_id=1,
                                                     category_id=1,
                                                     comment=u'CC',
                                                     date=self.get_today().isoformat(),
                                                     target_balance_id=''))
        self.assert200(response)
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, 30)

    def test_unit_add_income_transaction(self):
        self.repository.transactions.transaction_create(transaction_type_id=1,
                                                        amount=100,
                                                        balance_id=1,
                                                        category_id=1,
                                                        comment=u'Test income trans',
                                                        date=self.get_today())
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, 100)

    def test_unit_add_spending_transaction(self):
        self.repository.transactions.transaction_create(transaction_type_id=2,
                                                        amount=75,
                                                        balance_id=1,
                                                        category_id=2,
                                                        comment=u'Test spending trans',
                                                        date=self.get_today())
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, -75)

    def test_unit_transfer_with_same_currency(self):
        self.repository.accounts.account_create(1, u'CC', 1, 3, 100)
        self.repository.transactions.transaction_create(transaction_type_id=3,
                                                        amount=75,
                                                        balance_id=2,
                                                        category_id=None,
                                                        comment=u'Test transfer',
                                                        date=self.get_today(),
                                                        target_balance_id=1)
        bal1 = self.repository.balances.balance_get(1)
        bal2 = self.repository.balances.balance_get(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 25)

    def test_unit_transfer_with_different_currencies(self):
        self.repository.accounts.account_create(1, u'CC', 1, 1, 100)
        self.repository.transactions.transaction_create(transaction_type_id=3,
                                                        amount=3,
                                                        balance_id=2,
                                                        category_id=None,
                                                        comment=u'Test transfer 2',
                                                        date=self.get_today(),
                                                        child_to=1,
                                                        target_amount=75)
        bal1 = self.repository.balances.balance_get(1)
        bal2 = self.repository.balances.balance_get(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 97)

    def test_unit_transfer_with_different_currencies_2(self):
        self.repository.accounts.account_create(1, u'CC', 1, 5, 100)
        self.repository.transactions.transaction_create(transaction_type_id=3,
                                                        amount=50,
                                                        balance_id=2,
                                                        category_id=None,
                                                        comment=u'Test transfer 2',
                                                        date=self.get_today(),
                                                        target_balance_id=1,
                                                        target_amount=16.5)
        bal1 = self.repository.balances.balance_get(1)
        bal2 = self.repository.balances.balance_get(2)
        self.assertEqual(bal1.balance, 16.5)
        self.assertEqual(bal2.balance, 50)

    def test_unit_change_income_transaction_sum(self):
        self.repository.transactions.transaction_create(transaction_type_id=1,
                                                        amount=50,
                                                        balance_id=1,
                                                        category_id=2,
                                                        comment=u'',
                                                        date=self.get_today(),
                                                        child_to=1)
        self.repository.transactions.transaction_change(transaction_id=1,
                                                        transaction_type_id=1,
                                                        amount=40,
                                                        balance_id=1,
                                                        category_id=2,
                                                        comment=u'',
                                                        date=self.get_today())
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, 40)

    def test_unit_change_spending_transaction_sum(self):
        self.repository.transactions.transaction_create(transaction_type_id=2,
                                                        amount=50,
                                                        balance_id=1,
                                                        category_id=2,
                                                        comment=u'',
                                                        date=self.get_today())
        self.repository.transactions.transaction_change(transaction_id=1,
                                                        transaction_type_id=2,
                                                        amount=40,
                                                        balance_id=1,
                                                        category_id=2,
                                                        comment=u'',
                                                        date=self.get_today())
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, -40)

    def test_unit_change_transfer_transaction_sum(self):
        self.repository.accounts.account_create(1, u'CC', 1, 3, 100)
        self.repository.transactions.transaction_create(transaction_type_id=3,
                                                        amount=50,
                                                        balance_id=2,
                                                        category_id=None,
                                                        comment=u'',
                                                        date=self.get_today(),
                                                        target_balance_id=1)
        self.repository.transactions.transaction_change(transaction_id=1,
                                                        transaction_type_id=3,
                                                        amount=40,
                                                        balance_id=2,
                                                        category_id=None,
                                                        comment=u'',
                                                        date=self.get_today(),
                                                        target_balance_id=1)
        bal1 = self.repository.balances.balance_get(1)
        bal2 = self.repository.balances.balance_get(2)
        self.assertEqual(bal1.balance, 40)
        self.assertEqual(bal2.balance, 60)

    def test_unit_delete_income_transaction(self):
        trans_id = self.repository.transactions.transaction_create(transaction_type_id=1,
                                                                   amount=50,
                                                                   balance_id=1,
                                                                   category_id=2,
                                                                   comment=u'',
                                                                   date=self.get_today())
        self.repository.transactions.transaction_delete(trans_id)
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, 0)

    def test_unit_delete_spending_transaction(self):
        trans_id = self.repository.transactions.transaction_create(transaction_type_id=2,
                                                                   amount=50,
                                                                   balance_id=1,
                                                                   category_id=2,
                                                                   comment=u'',
                                                                   date=self.get_today())
        self.repository.transactions.transaction_delete(trans_id)
        bal = self.repository.balances.balance_get(1)
        self.assertEqual(bal.balance, 0)

    def test_unit_delete_transfer_transaction(self):
        self.repository.accounts.account_create(1, u'CC', 1, 5, 100)
        trans_id = self.repository.transactions.transaction_create(transaction_type_id=3,
                                                                   amount=50,
                                                                   balance_id=2,
                                                                   category_id=None,
                                                                   comment=u'',
                                                                   date=self.get_today(),
                                                                   target_balance_id=1)
        self.repository.transactions.transaction_delete(trans_id)
        bal1 = self.repository.balances.balance_get(1)
        bal2 = self.repository.balances.balance_get(2)
        self.assertEqual(bal1.balance, 0)
        self.assertEqual(bal2.balance, 100)
