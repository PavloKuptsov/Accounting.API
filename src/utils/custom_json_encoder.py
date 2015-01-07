from decimal import Decimal
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if hasattr(obj, 'isoformat'):
           return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)