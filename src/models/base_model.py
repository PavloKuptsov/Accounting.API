from datetime import date
from dateutil import parser



class BaseModel(object):

    def to_dict(self):
        result = {}
        for attr in self.__dir__():
            attribute = getattr(self, attr, u'')
            if isinstance(attribute, list):
                result[attr] = [(isinstance(i, BaseModel) and i.to_dict()) or i for i in attribute]
            elif isinstance(attribute, BaseModel):
                result[attr] = attribute.to_dict()
            else:
                result[attr] = attribute
        return result

    @classmethod
    def create(cls, data):
        obj = cls()
        for attr, value in data.items():
            attr = str(attr)
            try:
                if hasattr(obj, attr):
                    preprocess_method = getattr(obj, 'preprocess_' + attr) \
                        if hasattr(obj, 'preprocess_' + attr) else None
                    if callable(preprocess_method):
                        value = preprocess_method(value)
                    if not value and type(getattr(obj, attr)) == str:
                        value = u''
                    if not value and type(getattr(obj, attr)) == unicode:
                        value = u''
                    if value and type(getattr(obj, attr)) != type(value) and getattr(obj, attr) is not None:
                        if type(getattr(obj, attr)) is date:
                            value = parser.parse(value).date()
                        else:
                            value = type(getattr(obj, attr))(value)
                    setattr(obj, attr, value)
                else:
                    obj.attr = value
            except Exception, e:
                raise Exception('%s for \'%s\' attribute.' % (e.message, attr))
        return obj

    @staticmethod
    def __dir__():
        return []
