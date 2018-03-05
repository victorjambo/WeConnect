import  os
import unittest
from src import app


class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_review(self):
        pass

    def test_read_reviews(self):
        pass

    def test_update_review(self):
        pass

    def test_delete_business(self):
        pass


if __name__ == '__main__':
    unittest.main()
