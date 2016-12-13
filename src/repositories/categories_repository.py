# coding=utf-8

from config import DB
from models.category import Category


class CategoriesRepository(object):

    @staticmethod
    def categories_list(user_id):
        return Category.query.filter_by(user_id=user_id).all()

    @staticmethod
    def category_create(user_id, name, parent_category_id, type_id):
        cat = Category(user_id, name, parent_category_id, type_id)
        DB.session.add(cat)
        DB.session.commit()
        return cat.category_id

    @staticmethod
    def category_change(category_id, name, parent_category_id):
        category = Category.query.filter_by(category_id=category_id).first()
        category.name = name
        category.parent_category_id = parent_category_id
        DB.session.commit()

    @staticmethod
    def category_get(category_id):
        return Category.query.filter_by(category_id=category_id).first()

    @staticmethod
    def category_delete(category_id):
        category = CategoriesRepository.category_get(category_id)
        DB.session.delete(category)
        DB.session.commit()

    @staticmethod
    def category_is_a_duplicate(user_id, name, parent_category_id):
        cat = Category.query.filter_by(user_id=user_id, name=name, parent_category_id=parent_category_id).first()
        return bool(cat)
