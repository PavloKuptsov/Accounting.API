from sqlalchemy import Table, Column, Integer, String, MetaData, Numeric, Unicode, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

from account import Account
from balance import Balance
from category import Category
from currency import Currency
from tag import Tag
from transaction import Transaction


class DBHelper(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///C:\\accounting.sqlite', echo=True)
        self.metadata = MetaData()
        self.create_tables()
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session()

    def create_tables(self):
        account_table = Table('account',
                              self.metadata,
                              Column('account_id', Integer, primary_key=True),
                              Column('type_id', Integer),
                              Column('name', String),
                              Column('owner_id', Integer))
        balance_table = Table('balance',
                              self.metadata,
                              Column('balance_id', Integer, primary_key=True),
                              Column('account_id', Integer),
                              Column('currency_id', Integer),
                              Column('balance', Numeric(precision=2)))
        category_table = Table('category',
                               self.metadata,
                               Column('category_id', Integer, primary_key=True),
                               Column('name', Unicode(length=100)),
                               Column('parent_category_id', Integer),
                               Column('type_id', Integer))
        currency_table = Table('currency',
                               self.metadata,
                               Column('currency_id', Integer, primary_key=True),
                               Column('name', Unicode(length=100)),
                               Column('short_name', Unicode(length=3)))
        tag_table = Table('tag',
                          self.metadata,
                          Column('tag_id', Integer, primary_key=True),
                          Column('name', Unicode(length=100)))
        transaction_type_table = Table('transaction_type',
                                       self.metadata,
                                       Column('transaction_type_id', Integer, primary_key=True),
                                       Column('name', Unicode(length=100)))
        transaction_table = Table('transaction',
                                  self.metadata,
                                  Column('transaction_id', Integer, primary_key=True),
                                  Column('transaction_type_id', Integer),
                                  Column('amount', Numeric(precision=2)),
                                  Column('balance_id', Integer),
                                  Column('category_id', Integer),
                                  Column('comment', Unicode(length=255)),
                                  Column('date', Date),
                                  Column('exchange_rate', Numeric(precision=2), default=1),
                                  Column('child_to', Integer, default=None))
        self.metadata.create_all(self.engine)
        mapper(Account, account_table)
        mapper(Balance, balance_table)
        mapper(Category, category_table)
        mapper(Currency, currency_table)
        mapper(Tag, tag_table)
        mapper(Transaction, transaction_table)
