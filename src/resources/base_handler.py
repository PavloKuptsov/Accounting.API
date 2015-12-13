from flask.ext.restful import Resource
from utils.repository import Repository


class BaseHandler(Resource):

    def __init__(self):
        self.repository = Repository()
