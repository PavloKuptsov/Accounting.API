from datetime import datetime
from decimal import Decimal
from flask import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # SQLAlchemy lists
        if isinstance(obj, InstrumentedList):
            obj = [self.default(x) for x in obj]
        # SQLAlchemy model
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = self.default(data)
            # a json-encodable dict
            return fields

        if isinstance(obj, Decimal):
            return str(obj)

        if isinstance(obj, datetime):
            return obj.isoformat()
        # lists
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)

        return json.JSONEncoder.default(self, obj)
