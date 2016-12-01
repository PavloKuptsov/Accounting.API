from flask import g
from flask_restful import Resource

from config import auth
from utils.repository import Repository


class BaseHandler(Resource):

    def __init__(self):
        self.repository = Repository()


@auth.verify_password
def verify_password(username, password):
    repository = Repository()
    user = repository.user_search(username)
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
