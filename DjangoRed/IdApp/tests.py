from django.test import TestCase
from .db_query import get_comment_datasets, get_user_datasets

class get_ids_test(TestCase):
    def test_get_comment_datasets(self):
        r = get_comment_datasets()

        print(r)
        self.assertTrue(r)

    def test_get_user_datasets(self):
        r = get_user_datasets()

        print(r)
        self.assertTrue(r)