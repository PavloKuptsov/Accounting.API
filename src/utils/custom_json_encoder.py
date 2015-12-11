from decimal import Decimal
from flask.json import JSONEncoder

from base_model import BaseModel


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        if isinstance(obj, BaseModel):
            return obj.to_dict()
        return super(CustomJSONEncoder, self).default(obj)