from base_model import BaseModel


class Account(BaseModel):
    id = 0
    type_id = 0
    name = u''
    owner_id = 0
    default_currency_id = 0
    balances = []

    def __dir__(self):
        return ['id', 'type_id', 'name', 'owner_id', 'default_currency_id', 'balances']

    def preprocess_balances(self):
        pass