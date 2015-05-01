from datetime import datetime
from models.base_model import BaseModel


class Transaction(BaseModel):
    id = 0
    type_id = 0
    amount = 0.00
    balance_id = 0
    target_balance_id = 0
    previous_balance = 0.00
    category_id = 0
    comment = u''
    date = datetime.now().date()
    exchange_rate = 1.00

    def __dir__(self):
        return ['id', 'type_id', 'amount', 'balance_id', 'target_balance_id', 'previous_balance',
                'category_id', 'comment', 'date', 'exchange_rate']