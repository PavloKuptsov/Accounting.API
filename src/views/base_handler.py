from flask import jsonify
from flask.views import MethodView
from config import RESULT_STATUS, RESULT_RESPONSE, RESULT_ERRORS, RESPONSE_OK
from models.base_model import BaseModel
from utils.repository import Repository


class BaseHandler(MethodView):

    def __init__(self):
        self.errors = []
        self.repository = Repository()

    def json_response(self, model, status=RESPONSE_OK):
        dict = model and (isinstance(model, BaseModel) and model.to_dict()) or [i.to_dict() for i in model] or {}
        result = jsonify({
            RESULT_STATUS: status,
            RESULT_RESPONSE: dict,
            RESULT_ERRORS: self.errors
        })
        return result