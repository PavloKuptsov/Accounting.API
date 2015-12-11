from base_handler import BaseHandler


class AccountsHandler(BaseHandler):

    def dispatch_request(self):
        pass

    def get(self):
        accounts = self.repository.list_accounts()
        return accounts

    def post(self):
        pass
