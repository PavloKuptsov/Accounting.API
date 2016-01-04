from base_test import BaseTest
from test_data import URL_CATEGORIES, TEST_CATEGORIES_LIST


class TestCategories(BaseTest):

    def test_func_create_category(self):
        response = self.post(URL_CATEGORIES, dict(user_id=1, name=u'Salary', parent_category_id=0, type_id=1), True)
        self.assert_status(response, 201)

    def test_func_creating_duplicate_category_fails(self):
        response = self.post(URL_CATEGORIES, dict(user_id=1,
                                                  name=u'Sample income category',
                                                  parent_category_id=None,
                                                  type_id=1), True)
        self.assert400(response)

    def test_func_list_categories(self):
        response = self.get(URL_CATEGORIES, True)
        self.assert200(response)
        self.assertEquals(response.json, TEST_CATEGORIES_LIST)
