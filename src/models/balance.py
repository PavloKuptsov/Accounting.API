from models.base_model import BaseModel
from models.currency import Currency


class Balance(BaseModel):
    id = 0
    account_id = 0
    currency_id = 0
    balance = 0.0
    currency = Currency()

    def __dir__(self):
        return ['id', 'account_id', 'currency_id', 'balance', 'currency']
