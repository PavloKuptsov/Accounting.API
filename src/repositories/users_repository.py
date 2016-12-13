# coding=utf-8

from config import DB
from models.user import User


class UsersRepository(object):

    @staticmethod
    def user_create(username, password):
        user = User(username, password, [])
        user.hash_password(password)
        DB.session.add(user)
        DB.session.commit()
        return user.user_id

    @staticmethod
    def user_search(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def user_id_search(username):
        return UsersRepository.user_search(username).user_id

    @staticmethod
    def user_by_id_search(user_id):
        return User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def user_delete(user_id):
        user = User.query.filter_by(user_id=user_id).first()
        DB.session.delete(user)
        DB.session.commit()

    @staticmethod
    def user_change_password(user_id, password):
        user = User.query.filter_by(user_id=user_id).first()
        user.hash_password(password)
        DB.session.commit()

