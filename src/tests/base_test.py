from flask import Flask
from flask.ext.testing import TestCase

from config import DB


class BaseTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://C:\\accounting_test.sqlite"
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        DB.create_all()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()
