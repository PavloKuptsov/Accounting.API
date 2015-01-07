from storm.locals import *
from models.base_model import BaseModel


class Category(BaseModel):
    __storm_table__ = 'category'
    id = Int(primary=True)
    name = Unicode()
    parent_category_id = Int()
    type_id = 0
    parent_category = Reference(parent_category_id, id)

    def __dir__(self):
        return ['id', 'name', 'parent_category_id', 'type_id']