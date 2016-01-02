from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship


from account import Account
from config import DB


class User(DB.Model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    password = Column(String(128))
    accounts = relationship(Account, cascade="all,delete")

    def __init__(self, username, password, accounts):
        self.username = username
        self.password = password
        self.accounts = accounts

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    @staticmethod
    def __dir__():
        return ['user_id', 'username', 'password', 'accounts']

    def __repr__(self):
        return 'User: \n user_id %s, \n username %s, \n password %s, \n accounts %s' % \
               (self.user_id, self.username, self.password, self.accounts)
