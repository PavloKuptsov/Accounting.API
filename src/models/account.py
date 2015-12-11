from base_model import BaseModel


class Account(BaseModel):
    def __init__(self, account_id, type_id, name, owner_id, default_currency_id, balances):
        self.account_id = account_id
        self.type_id = type_id
        self.name = name
        self.owner_id = owner_id
        self.default_currency_id = default_currency_id
        self.balances = balances

    @staticmethod
    def __dir__():
        return ['id', 'type_id', 'name', 'owner_id', 'default_currency_id', 'balances']
