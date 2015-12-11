from base_model import BaseModel


class Balance(BaseModel):
    def __init__(self, balance_id, account_id, currency_id, balance, currency):
        self.balance_id = balance_id
        self.account_id = account_id
        self.currency_id = currency_id
        self.balance = balance
        self.currency = currency

    @staticmethod
    def __dir__():
        return ['balance_id', 'account_id', 'currency_id', 'balance', 'currency']
