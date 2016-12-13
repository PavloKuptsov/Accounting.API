from sqlalchemy import Column, Integer, Unicode, ForeignKey, Boolean
from config import DB


class Category(DB.Model):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    name = Column(Unicode(100))
    parent_category_id = Column(Integer)
    type_id = Column(Integer, ForeignKey('category_type.type_id'))
    is_favorite = Column(Boolean, default=False)

    def __init__(self, user_id, name, parent_category_id, type_id):
        self.user_id = user_id
        self.name = name
        self.parent_category_id = parent_category_id
        self.type_id = type_id

    @staticmethod
    def __dir__():
        return ['category_id', 'name', 'parent_category_id', 'type_id', 'is_favorite']

    def __repr__(self):
        return '<Category id=%s, type_id=%s, name=%s, parent_id=%s>' % \
               (self.category_id, self.type_id, self.name, self.parent_category_id)
