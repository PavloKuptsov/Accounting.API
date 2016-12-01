from resources.base_handler import BaseHandler
from config import auth


class BalanceHandler(BaseHandler):

    @auth.login_required
    def put(self, balance_id):
        pass

    @auth.login_required
    def delete(self, balance_id):
        pass
