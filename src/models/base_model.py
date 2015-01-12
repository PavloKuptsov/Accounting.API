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
        object = cls()
        for attr, value in data.items():
            attr = str(attr)
            try:
                if hasattr(object, attr):
                    preprocess_method = getattr(object, 'preprocess_' + attr) \
                        if hasattr(object, 'preprocess_' + attr) else None
                    if callable(preprocess_method):
                        value = preprocess_method(value)
                    if not value and type(getattr(object, attr)) == str:
                        value = u''
                    if not value and type(getattr(object, attr)) == unicode:
                        value = u''
                    if value and type(getattr(object, attr)) != type(value) and getattr(object, attr) is not None:
                        if type(getattr(object, attr)) is date:
                            value = parser.parse(value).date()
                        else:
                            value = type(getattr(object, attr))(value)
                    setattr(object, attr, value)
                else:
                    object.attr = value
            except Exception, e:
                raise Exception('%s for \'%s\' attribute.' % (e.message, attr))
        return object

    def __dir__(self):
        return []