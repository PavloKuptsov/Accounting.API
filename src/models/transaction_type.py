# from sqlalchemy import Column, Integer, Unicode
#
# from config import DB
#
#
# class TransactionType(DB.Model):
#     __tablename__ = 'transaction_type'
#
#     transaction_type_id = Column(Integer, primary_key=True),
#     name = Column(Unicode(100))
#
#     def __init__(self, transaction_type_id, name):
#         self.transaction_type_id = transaction_type_id
#         self.name = name
#
#     @staticmethod
#     def __dir__():
#         return ['transaction_type_id', 'name']
