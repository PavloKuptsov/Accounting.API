# coding=utf-8
from decimal import Decimal

from config import DB
from models.account import Account
from models.balance import Balance
from models.global_variables import TRANSACTION_TYPE_INCOME, TRANSACTION_TYPE_SPENDING, TRANSACTION_TYPE_TRANSFER
from models.transaction import Transaction


class TransactionsRepository(object):

    @staticmethod
    def transaction_create(transaction_type_id, amount, balance_id, category_id, comment, date,
                           target_balance_id=None, child_to=None, target_amount=None):
        amount = Decimal(amount)
        if transaction_type_id == TRANSACTION_TYPE_TRANSFER and target_amount is None:
            target_amount = amount
        trans = Transaction(transaction_type_id, amount, balance_id, category_id, comment, date, child_to)
        balance = Balance.query.filter_by(balance_id=balance_id).first()

        DB.session.add(trans)
        DB.session.flush()

        if transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance += amount
        elif transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance -= amount
        elif transaction_type_id == TRANSACTION_TYPE_TRANSFER and not child_to:
            balance.balance -= amount
            TransactionsRepository.transaction_create(transaction_type_id=transaction_type_id,
                                                      amount=target_amount,
                                                      balance_id=target_balance_id,
                                                      category_id=None,
                                                      comment=None,
                                                      date=None,
                                                      child_to=trans.transaction_id)
        else:
            balance.balance += amount
        DB.session.commit()
        return trans.transaction_id

    @staticmethod
    def transaction_delete(transaction_id):
        trans = Transaction.query.filter_by(transaction_id=transaction_id).first()
        balance = Balance.query.filter_by(balance_id=trans.balance_id).first()

        if trans.transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance -= trans.amount
        elif trans.transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance += trans.amount
        else:
            child_trans = Transaction.query.filter_by(child_to=trans.transaction_id).first()
            target_balance = Balance.query.filter_by(balance_id=child_trans.balance_id).first()
            balance.balance += trans.amount
            target_balance.balance -= child_trans.amount
            DB.session.delete(child_trans)
        DB.session.delete(trans)
        DB.session.commit()

    @staticmethod
    def transaction_change(transaction_id, transaction_type_id, amount, balance_id, category_id, comment, date,
                           target_balance_id=None):
        amount = Decimal(amount)
        trans = Transaction.query.filter_by(transaction_id=transaction_id).first()
        balance = Balance.query.filter_by(balance_id=balance_id).first()

        if trans.transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance -= trans.amount
        elif trans.transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance += trans.amount
        elif trans.transaction_type_id == TRANSACTION_TYPE_TRANSFER:
            child_trans = Transaction.query.filter_by(child_to=trans.transaction_id).first()
            target_balance = Balance.query.filter_by(balance_id=child_trans.balance_id).first()
            balance.balance += trans.amount
            target_balance.balance -= child_trans.amount
            DB.session.delete(child_trans)

        trans.transaction_type_id = transaction_type_id
        trans.amount = amount
        trans.balance_id = balance_id
        trans.category_id = category_id
        trans.comment = comment
        trans.date = date

        if transaction_type_id == TRANSACTION_TYPE_INCOME:
            balance.balance += amount
        elif transaction_type_id == TRANSACTION_TYPE_SPENDING:
            balance.balance -= amount
        elif transaction_type_id == TRANSACTION_TYPE_TRANSFER:
            balance.balance -= amount
            TransactionsRepository.transaction_create(transaction_type_id=transaction_type_id,
                                                      amount=amount,
                                                      balance_id=target_balance_id,
                                                      category_id=None,
                                                      comment=None,
                                                      date=None,
                                                      child_to=trans.transaction_id,
                                                      target_balance_id=None)
        else:
            balance.balance += amount
        DB.session.commit()
        return trans.transaction_id

    @staticmethod
    def transaction_search_by_account(account_id):
        balance_ids = Balance.query.with_entities(Balance.balance_id).filter_by(account_id=account_id).all()
        transactions = Transaction.query.filter(Transaction.balance_id.in_(balance_ids)).all()
        return transactions

    @staticmethod
    def transactions_search_by_user_id(user_id):
        account_ids = Account.query.with_entities(Account.account_id).filter_by(user_id=user_id).all()
        balance_ids = Balance.query.with_entities(Balance.balance_id).filter(Balance.account_id.in_(account_ids)).all()
        transactions = Transaction.query.filter(Transaction.balance_id.in_(balance_ids)).all()
        return transactions

    @staticmethod
    def transactions_search_by_category_id(category_id):
        return Transaction.query.filter_by(category_id=category_id).all()
