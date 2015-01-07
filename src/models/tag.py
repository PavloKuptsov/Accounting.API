from storm.locals import *
from models.base_model import BaseModel


class Tag(BaseModel):
    __storm_table__ = 'tag'
    id = Int(primary=True)
    name = Unicode()

    def __dir__(self):
        return ['id', 'name']