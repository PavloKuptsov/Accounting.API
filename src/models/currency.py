from models.base_model import BaseModel


class Currency(BaseModel):
    id = 0
    name = u''
    short_name = u''
    exchange_rate = 0.0

    def __dir__(self):
        return ['id', 'name', 'short_name', 'exchange_rate']
