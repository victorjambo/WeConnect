import json
import unittest
from versions import app, review_instance, business_instance, user_instance


class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.new_review = {
            "title": "Friday 13th",
            "desc": "biz 1 user 1 id 5"
        }
        self.new_user_info = {
            "username": "robert",
            "email": "victor.mutai@students.jkuat.ac.ke",
            "password": "password"
        }
        self.user_login_info = {
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
            data=json.dumps(self.user_login_info),
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

    def test_cannot_delete_review(self):
        """test different user deleting review
        """
        new_user = {
            "username": "hotpoint",
            "email": "victor.mutai@nbo.samadc.org",
            "password": "password"
        }
        new_user_login = {
            "username": "hotpoint",
            "password": "password"
        }
        business_data = {
            "name": "Crowns paints",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }
        self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        response_login = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(new_user_login),
            content_type='application/json'
        )
        token = json.loads(response_login.get_data(as_text=True))['token']

        self.app.post(
            '/api/v1/businesses',
            data=json.dumps(business_data),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        response = self.app.post(
            '/api/v1/business/1/reviews',
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        response = self.app.delete(
            '/api/v1/business/1/reviews/1',
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response.status_code, 401)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['warning'], 'Not Allowed')

    def test_delete_review(self):
        """Test deleting business twice
        """
        business_data = {
            "name": "Crown",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }

        self.app.post(
            '/api/v1/businesses',
            data=json.dumps(business_data),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )

        self.app.post(
            '/api/v1/business/1/reviews',
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )

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

    def tearDown(self):
        """Clear list"""
        user_instance.users.clear()
        business_instance.businesses.clear()
        review_instance.reviews.clear()


if __name__ == '__main__':
    unittest.main()
