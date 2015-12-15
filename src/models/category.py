# from sqlalchemy import Column, Integer, Unicode
#
# from config import DB
#
#
# class Category(DB.Model):
#     __tablename__ = 'category'
#     category_id = Column(Integer, primary_key=True)
#     name = Column(Unicode(100))
#     parent_category_id = Column(Integer)
#     type_id = Column(Integer)
#
#     def __init__(self, category_id, name, parent_category_id, type_id, new_category_id):
#         self.category_id = category_id
#         self.name = name
#         self.parent_category_id = parent_category_id
#         self.type_id = type_id
#         self.new_category_id = new_category_id
#
#     @staticmethod
#     def __dir__():
#         return ['category_id', 'name', 'parent_category_id', 'type_id', 'new_category_id']
