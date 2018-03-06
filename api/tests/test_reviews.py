import  os
import json
import unittest
from v1 import app, reviews


class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.new_review = {
            "title": "Friday 13th",
            "desc": "biz 1 user 1 id 5",
        }

    def test_create_review(self):
        """Create new review for a business
        """
        initial_count = len(reviews)
        response = self.app.post(
            '/api/businesses/1/reviews',
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
        resp = self.app.get('/api/businesses/1/reviews')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(reviews), 0)

        response = self.app.get('/api/businesses/reviews')
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        """Test deleting business twice
        """
        response = self.app.delete('/api/businesses/1/reviews/1')
        self.assertEqual(response.status_code, 200)

        # delete already deleted review
        response = self.app.delete('/api/businesses/1/reviews/1')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
