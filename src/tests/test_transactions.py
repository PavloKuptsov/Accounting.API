from base_test import BaseTest


class TestTransactions(BaseTest):

    def test_func_add_transaction(self):
        pass

    def test_func_delete_transaction(self):
        pass

    def test_func_change_transaction(self):
        pass

    def test_unit_add_input_transaction(self):
        self.repository.add_transaction(1, 100, 1, 1, u'Test income trans', self.get_today(), 1, None, None)
        bal = self.repository.get_balance(1)
        self.assertEqual(bal.balance, 100)

    def test_unit_add_spending_transaction(self):
        self.repository.add_transaction(2, 75, 1, 2, u'Test spending trans', self.get_today(), 1, None, None)
        bal = self.repository.get_balance(1)
        self.assertEqual(bal.balance, -75)

    def test_unit_transfer_with_same_currency(self):
        self.repository.add_account(1, u'CC', 1, 3, 100)
        # print(self.repository.list_user_accounts(1))
        self.repository.add_transaction(3, 75, 2, None, u'Test transfer', self.get_today(), 1, None, 1)
        bal1 = self.repository.get_balance(1)
        bal2 = self.repository.get_balance(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 25)

    def test_unit_transfer_with_different_currencies(self):
        self.repository.add_account(1, u'CC', 1, 1, 100)
        # print(self.repository.list_user_accounts(1))
        self.repository.add_transaction(3, 3, 2, None, u'Test transfer 2', self.get_today(), 25, None, 1)
        bal1 = self.repository.get_balance(1)
        bal2 = self.repository.get_balance(2)
        self.assertEqual(bal1.balance, 75)
        self.assertEqual(bal2.balance, 97)


