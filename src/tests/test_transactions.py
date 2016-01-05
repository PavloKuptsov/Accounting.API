from base_test import BaseTest


class TestTransactions(BaseTest):

    def test_func_add_transaction(self):
        pass

    def test_func_delete_transaction(self):
        pass

    def test_func_change_transaction(self):
        pass

    def test_unit_add_input_transaction(self):
        self.repository.transaction_create(1, 100, 1, 1, u'Test income trans', self.get_today(), 1, None, None)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, 100)

    def test_unit_add_spending_transaction(self):
        self.repository.transaction_create(2, 75, 1, 2, u'Test spending trans', self.get_today(), 1, None, None)
        bal = self.repository.balance_get(1)
        self.assertEqual(bal.balance, -75)

    def test_unit_transfer_with_same_currency(self):
        self.repository.account_create(1, u'CC', 1, 3, 100)
        self.repository.transaction_create(3, 75, 2, None, u'Test transfer', self.get_today(), 1, None, 1)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 25)

    def test_unit_transfer_with_different_currencies(self):
        self.repository.account_create(1, u'CC', 1, 1, 100)
        self.repository.transaction_create(3, 3, 2, None, u'Test transfer 2', self.get_today(), 25, None, 1)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 97)

    def test_unit_transfer_with_different_currencies_2(self):
        self.repository.account_create(1, u'CC', 1, 5, 100)
        self.repository.transaction_create(3, 50, 2, None, u'Test transfer 2', self.get_today(), 0.33, None, 1)
        bal1 = self.repository.balance_get(1)
        bal2 = self.repository.balance_get(2)
        self.assertEqual(bal1.balance, 16.5)
        self.assertEqual(bal2.balance, 50)


