from account import Account
from balance import Balance
from config import DB
from user import User


class Repository(object):

    def create_user(self, username, password):
        account = Account(1, u'Cash', 1, 0)
        user = User(username, password, [])
        user.hash_password(password)
        user.accounts = [account]
        DB.session.add(user)
        DB.session.commit()
        return user.user_id

    def search_user(self, username):
        return User.query.filter(User.username == username).first()

    def search_user_id(self, username):
        return self.search_user(username).user_id

    def list_user_accounts(self, user_id):
        accounts = Account.query.filter_by(user_id=user_id).all()
        return accounts

    def add_account(self, type_id, name, user_id, currency_id, balance):
        user = User.query.filter(User.user_id == user_id).first()
        acc = Account(type_id, name, currency_id, balance)
        user.accounts.append(acc)
        DB.session.commit()
        return acc.account_id

    def add_balance(self, account_id, currency_id, balance):
        acc = Account.query.filter(Account.account_id == account_id).first()
        bal = Balance(currency_id, balance)
        acc.balances.append(bal)
        DB.session.commit()
        return bal.balance_id

    def delete_account(self, account_id):
        res = Account.query.filter_by(account_id=account_id).delete()
        return res

    def get_account(self, account_id):
        return Account.query.filter_by(account_id=account_id).first()

    def change_account(self, account_id, type_id, name):
        acc = self.get_account(account_id)
        acc.type_id = type_id
        acc.name = name
        DB.session.commit()
