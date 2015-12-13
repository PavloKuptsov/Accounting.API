from account import Account
from config import DB


class Repository(object):

    def list_accounts(self):
        # self.add_account()
        account = DB.session.query(Account).all()
        return account

    def add_account(self):
        acc1 = Account(None, 1, 'Cash', 1, 1, [])
        DB.session.add(acc1)
        DB.session.commit()
