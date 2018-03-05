import  os
import json
import unittest
from v1 import app, reviews


class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.new_review = {
            "id": "5",
            "title": "Friday 13th",
            "desc": "biz 1 user 1 id 5",
            "business_id": "1",
            "user_id": "1"
        }

    def test_create_review(self):
        """Create new review for a business
        """
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
        """Get reviews for business
        """
        resp = self.app.get('/api/businesses')
        self.assertEqual(resp.status_code, 200)

    def test_update_review(self):
        """Update business infor
        """
        update_review = {
            "id": "5",
            "title": "Some thing new",
            "desc": "biz 1 user 1 id 5",
            "business_id": "1",
            "user_id": "1"
        }
        resp = self.app.put(
            '/api/business/5/reviews',
            data=json.dumps(update_review),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 202)

    def test_delete_business(self):
        """Test deleting business twice
        """
        response = self.app.delete('/api/business/5/reviews')
        self.assertEqual(response.status_code, 200)

        # delete already deleted review
        response = self.app.delete('/api/business/5/reviews')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
