import  os
import json
import unittest
from v1 import app, reviews


class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.new_review = {
            "id": "5",
            "title": "Good work",
            "desc": "biz 1 user 1 id 2",
            "business_id": "1",
            "user_id": "1"
        }

    def test_create_review(self):
        initial_count = len(reviews)
        response = self.app.post(
            '/api/businesses',
            data=json.dumps(self.new_review),
            content_type='application/json'
        )
        final_count = len(reviews)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(final_count - initial_count, 1)

    def test_read_reviews(self):
        pass

    def test_update_review(self):
        pass

    def test_delete_business(self):
        pass


if __name__ == '__main__':
    unittest.main()
