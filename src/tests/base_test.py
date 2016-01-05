import json

import base64

from datetime import datetime
from flask import Flask
from flask.ext.restful import Api
from flask.ext.testing import TestCase
from werkzeug.datastructures import Headers

from config import DB, TestConfig
from repository import Repository
from test_data import TEST_USERNAME, TEST_PASSWORD
from urls import rules


class BaseTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestConfig)
        DB.init_app(app)
        api = Api(app)
        for rule in rules:
            api.add_resource(rule.view, rule.url)
        return app

    def setUp(self):
        DB.create_all()
        self.repository = Repository()
        self.repository.create_initial_testing_data()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()

    def create_valid_account(self):
        self.repository.account_create(1, u'Cash', 1, 1, 15.5)

    def create_other_valid_account(self):
        self.repository.account_create(2, u'CC', 1, 1, 25)

    def create_valid_balance(self):
        self.repository.balance_create(1, 1, 25.5)

    def get_auth_headers(self):
        h = Headers()
        h.add('Authorization',
              'Basic ' + base64.b64encode(TEST_USERNAME + ':' + TEST_PASSWORD))
        return h

    def get(self, url):
        response = self.client.get(url,
                                   headers=self.get_auth_headers() or '')
        return response

    def get_no_auth(self, url):
        response = self.client.get(url)
        return response

    def post(self, url, data):
        response = self.client.post(url,
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers=self.get_auth_headers() or '')
        return response

    def post_no_auth(self, url, data):
        response = self.client.post(url,
                                    data=json.dumps(data),
                                    content_type='application/json')
        return response

    def put(self, url, data):
        response = self.client.put(url,
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   headers=self.get_auth_headers() or '')
        return response

    def delete(self, url):
        response = self.client.delete(url,
                                      headers=self.get_auth_headers() or '')
        return response

    def get_today(self):
        return datetime.now().date()

    def assertErrorTextEquals(self, response, error):
        self.assertEquals(response.json, dict(error=error))
