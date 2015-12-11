from base_model import BaseModel


class Currency(BaseModel):
    def __init__(self, currency_id, name, short_name):
        self.currency_id = currency_id
        self.name = name
        self.short_name = short_name

    @staticmethod
    def __dir__():
        return ['currency_id', 'name', 'short_name']
