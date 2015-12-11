from flask.ext.restful import Resource
from utils.repository import Repository


class BaseHandler(Resource):

    def dispatch_request(self):
        pass

    def __init__(self):
        self.errors = []
        self.repository = Repository()
