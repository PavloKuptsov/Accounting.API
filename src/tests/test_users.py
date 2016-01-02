from base_test import BaseTest
from test_data import TEST_USERNAME2, TEST_CREDENTIALS_DICT, TEST_CREDENTIALS_DICT2


class TestUsers(BaseTest):

    def test_func_user_creation(self):
        response = self.post('/api/signup/', TEST_CREDENTIALS_DICT2, False)
        self.assert_status(response, 201)

    def test_func_user_created(self):
        self.post('/api/signup/', TEST_CREDENTIALS_DICT2, True)
        user = self.repository.search_user(TEST_USERNAME2)
        self.assertTrue(user and user.username == TEST_USERNAME2)

    def test_func_duplicate_user_creation_fails(self):
        response = self.post('/api/signup/', TEST_CREDENTIALS_DICT, True)
        self.assert400(response, message='User already exists')

    # def test_user_data_wiped(self):
    #     pass
    #
    # def test_user_removed(self):
    #     pass
