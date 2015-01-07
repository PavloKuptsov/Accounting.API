from storm.locals import *
from models.base_model import BaseModel


class TransactionType(BaseModel):
    __storm_table__ = 'transaction_type'
    id = Int(primary=True)
    name = Unicode()

    def __dir__(self):
        return ['id', 'name']