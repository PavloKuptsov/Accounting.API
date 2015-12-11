from base_model import BaseModel


class Tag(BaseModel):
    def __init__(self, tag_id, name):
        self.tag_id = tag_id
        self.name = name

    @staticmethod
    def __dir__():
        return ['tag_id', 'name']
