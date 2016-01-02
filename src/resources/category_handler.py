# from flask import request
# from base_handler import BaseHandler
# from models.category import Category
#
#
# class CategoryHandler(BaseHandler):
#     def put(self):
#         data = request.form
#         category = Category.create(data)
#         result = self.repository.change_category(category)
#         return self.json_response(result)
#
#     def delete(self, id):
#         result = self.repository.delete_category(id)
#         return self.json_response(result)
