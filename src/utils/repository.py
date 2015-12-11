from account import Account
from dbhelper import DBHelper


class Repository(object):
    db = DBHelper()

    def list_accounts(self):
        account = self.db.get_session().query(Account).all()
        return account

    def add_account(self):
        acc1 = Account(None, 1, 'Cash', 1, 1, [1])
        session = self.db.get_session()
        session.add(acc1)
        session.commit()
