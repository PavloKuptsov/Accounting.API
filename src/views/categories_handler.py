from base_handler import BaseHandler


class CategoriesHandler(BaseHandler):
    def get(self):
        categories = self.repository.list_categories()
        return self.json_response(categories)

    def post(self):
        pass
