from base_test import BaseTest
from test_data import TEST_USERNAME2, TEST_CREDENTIALS_DICT, TEST_CREDENTIALS_DICT2, URL_USERS, url_user


class TestUsers(BaseTest):

    def test_func_user_created(self):
        response = self.post_no_auth(URL_USERS, TEST_CREDENTIALS_DICT2)
        self.assert_status(response, 201)
        user = self.repository.user_search(TEST_USERNAME2)
        self.assertTrue(user and user.username == TEST_USERNAME2)

    def test_func_duplicate_user_creation_fails(self):
        response = self.post(URL_USERS, TEST_CREDENTIALS_DICT)
        self.assert400(response)

    def test_func_user_removed(self):
        response = self.delete(url_user(1))
        self.assert200(response)
        response = self.get(url_user(1))
        self.assert401(response)

    def test_func_access_denied(self):
        response = self.get(url_user(2))
        self.assert401(response)

    def test_func_password_changed(self):
        response = self.put(url_user(1), {'old_password': 'test_password', 'new_password': 'password2'})
        self.assert200(response)
        response = self.get(url_user(1))
        self.assert401(response)

    # def test_user_data_wiped(self):
    #     pass
    #
