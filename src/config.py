from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from utils.custom_json_encoder import CustomJSONEncoder

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'accounting'
DB_NAME_TEST = 'accounting_test'
DB_USER = 'accounting'
DB_PASSWORD = 'accounting'

RESPONSE_OK = 200
RESPONSE_BAD_REQUEST = 400
RESPONSE_CREATED = 201
RESPONSE_NOT_FOUND = 404
RESPONSE_SERVER_ERROR = 500

DB = SQLAlchemy()
auth = HTTPBasicAuth()


class DevConfig(object):
    RESTFUL_JSON = {'cls': CustomJSONEncoder}
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(object):
    RESTFUL_JSON = {'cls': CustomJSONEncoder}
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME_TEST)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

