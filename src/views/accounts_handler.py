from base_handler import BaseHandler


class AccountsHandler(BaseHandler):
    def get(self):
        accounts = self.repository.list_accounts()
        return self.json_response(accounts)

    def post(self):
        pass
