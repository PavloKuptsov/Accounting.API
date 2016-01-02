# from flask import request
# from base_handler import BaseHandler
# from models.category import Category
#
#
# class CategoriesHandler(BaseHandler):
#     def get(self):
#         categories = self.repository.list_categories()
#         return self.json_response(categories)
#
#     def post(self):
#         data = request.form
#         category = Category.create(data)
#         result = self.repository.create_category(category)
#         return self.json_response(result)
