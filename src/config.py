from flask.ext.sqlalchemy import SQLAlchemy

from custom_json_encoder import CustomJSONEncoder

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'accounting'
DB_USER = 'accounting'
DB_PASSWORD = 'accounting'

RESPONSE_OK = 200
RESPONSE_BAD_REQUEST = 400
RESPONSE_CREATED = 201
RESPONSE_NOT_FOUND = 404
RESPONSE_SERVER_ERROR = 500

RESULT_STATUS = 'status'
RESULT_RESPONSE = 'response'
RESULT_ERRORS = 'errors'

DB = SQLAlchemy()


class MyConfig(object):
    RESTFUL_JSON = {'cls': CustomJSONEncoder}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\accounting.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
