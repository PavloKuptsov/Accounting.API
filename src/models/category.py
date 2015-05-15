from models.base_model import BaseModel


class Category(BaseModel):
    id = 0
    name = u''
    parent_category_id = None
    type_id = 0
    new_category_id = 0

    def __dir__(self):
        return ['id', 'name', 'parent_category_id', 'type_id', 'new_category_id']