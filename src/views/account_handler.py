from base_handler import BaseHandler


class AccountHandler(BaseHandler):
    def get(self, id):
        account = self.repository.get_account(id)
        return self.json_response(account)

    def post(self):
        pass

    def put(self):
        pass