from models.base_model import BaseModel


class DatabaseOperationResult(BaseModel):
    success = False
    id = None

    def __init__(self, success, id):
        self.success = success
        self.id = id

    def get_created_id(self):
        return self.id

    def __dir__(self):
        return ['success', 'id']