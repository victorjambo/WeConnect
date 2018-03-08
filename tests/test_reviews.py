import  os
import json
import unittest
from versions import app, review_instance


class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.new_review = {
            "title": "Friday 13th",
            "desc": "biz 1 user 1 id 5"
        }
        self.new_user_info = {
            "username": "robert",
            "password": "password"
        }
        self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        resp = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        self.token = json.loads(resp.get_data(as_text=True))['token']

    def test_create_review(self):
        """Create new review for a business
        """
        initial_count = len(review_instance.reviews)
        response = self.app.post(
            '/api/v1/business/1/reviews',
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        final_count = len(review_instance.reviews)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)

        output = json.loads(response.get_data(as_text=True))['success']
        self.assertEqual(output, 'review successfully created')

        self.assertEqual(review_instance.reviews[0]['title'], 'Friday 13th')

    def test_read_reviews(self):
        """Get reviews for business
        """
        self.app.post(
            '/api/v1/business/1/reviews',
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        resp = self.app.get('/api/v1/business/1/reviews')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(review_instance.reviews), 0)

        response = self.app.get(
            '/api/v1/businesses/reviews',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['Reviews']
        self.assertEqual(output[0]['title'], 'Friday 13th')

    def test_delete_review(self):
        """Test deleting business twice
        """
        initial = len(review_instance.reviews)
        response1 = self.app.delete(
            '/api/v1/business/1/reviews/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        final = len(review_instance.reviews)
        self.assertEqual(response1.status_code, 200)

        output1 = json.loads(response1.get_data(as_text=True))['success']
        self.assertEqual(output1, 'review deleted')

        self.assertEqual(initial - final, 1)

        # delete already deleted review
        response = self.app.delete(
            '/api/v1/business/1/reviews/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response.status_code, 404)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Review not found')


if __name__ == '__main__':
    unittest.main()
