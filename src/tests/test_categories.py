from tests.base_test import BaseTest
from tests.test_data import URL_CATEGORIES, url_category

TEST_CATEGORIES_LIST = [{'category_id': 1,
                         'name': u'Sample income category',
                         'parent_category_id': None,
                         'type_id': 1,
                         'is_favorite': False},
                        {'category_id': 2,
                         'name': u'Sample spending category',
                         'parent_category_id': None,
                         'type_id': 2,
                         'is_favorite': False},
                        {'category_id': 3,
                         'name': u'Sample child spending category',
                         'parent_category_id': 2,
                         'type_id': 2,
                         'is_favorite': False}]


class TestCategories(BaseTest):

    def test_func_create_category(self):
        response = self.post(URL_CATEGORIES, dict(user_id=1, name=u'Salary', parent_category_id=0, type_id=1))
        self.assert_status(response, 201)

    def test_func_creating_duplicate_category_fails(self):
        response = self.post(URL_CATEGORIES, dict(user_id=1,
                                                  name=u'Sample income category',
                                                  parent_category_id=None,
                                                  type_id=1))
        self.assert400(response)
        self.assertErrorTextEquals(response, 'Category already exists')

    def test_func_list_categories(self):
        response = self.get(URL_CATEGORIES)
        self.assert200(response)
        self.assertEquals(response.json, TEST_CATEGORIES_LIST)

    def test_func_change_category(self):
        self.post(URL_CATEGORIES, dict(user_id=1, name=u'Salary', parent_category_id=0, type_id=1))
        response = self.put(url_category(4), dict(name=u'Income child category', parent_category_id=1))
        self.assert200(response)

    def test_func_change_category_parent_to_other_type_fails(self):
        response = self.put(url_category(3), dict(name=u'Sample child spending category', parent_category_id=1))
        self.assert400(response)
        self.assertErrorTextEquals(response, 'You cannot change type of category')

    def test_func_delete_category(self):
        response = self.delete(url_category(3))
        self.assert200(response)

    def test_func_deletion_of_used_category_fails(self):
        self.repository.transactions.transaction_create(2, 100, 1, 3, u'', self.get_today(), None, None)
        response = self.delete(url_category(3))
        self.assert400(response)
        self.assertErrorTextEquals(response, 'Cannot delete category which has transactions')

    def test_unit_rename_category(self):
        self.repository.categories.category_change(3, u'Renamed category', 2)
        cat = self.repository.categories.category_get(3)
        self.assertEqual(cat.name, u'Renamed category')

    def test_unit_change_category_parent(self):
        self.repository.categories.category_change(3, u'Sample child spending category', 0)
        cat = self.repository.categories.category_get(3)
        self.assertEqual(cat.parent_category_id, 0)

    def test_unit_delete_category(self):
        self.repository.categories.category_delete(3)
        category = self.repository.categories.category_get(3)
        self.assertEqual(category, None)
