# from sqlalchemy import Column, Integer, Unicode
#
# from config import DB
#
#
# class Tag(DB.Model):
#     __tablename__ = 'tag'
#
#     tag_id = Column(Integer, primary_key=True)
#     name = Column(Unicode(100))
#
#     def __init__(self, tag_id, name):
#         self.tag_id = tag_id
#         self.name = name
#
#     @staticmethod
#     def __dir__():
#         return ['tag_id', 'name']
