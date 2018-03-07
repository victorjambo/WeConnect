import os
import unittest
import json
from v1 import app, business_instance


class TestBusiness(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.new_business_info = {
            "name": "Crown",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }
        self.update_business_info = {
            "name": "Crown paints",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }
        self.new_user_info = {
            "username": "robert",
            "password": "password"
        }
        self.app.post(
            '/api/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        resp = self.app.post(
            '/api/auth/login',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        self.token = json.loads(resp.get_data(as_text=True))['token']

    def test_read_all_businesses(self):
        """Test if can access endpoint for all businesses
        """
        response = self.app.get('/api/businesses')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(business_instance.businesses), 0)

    def test_create_business(self):
        """Test if can register new business
        """
        initial_business_count = len(business_instance.businesses)
        response = self.create_business()
        final_business_count = len(business_instance.businesses)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(final_business_count - initial_business_count, 1)

    def test_cannot_read_one_business(self):
        """Test route for single business that doesn't exist
        """
        self.create_business()
        response = self.app.get('/api/businesses/45')
        self.assertEqual(response.status_code, 404)

    def test_read_no_business(self):
        response = self.app.get('/api/businesses/60')
        self.assertEqual(response.status_code, 404)

    def test_cannot_update_business(self):
        """Test Update business info for non existing business
        """
        resp = self.app.put(
            '/api/businesses/45',
            data=json.dumps(self.update_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_business(self):
        response = self.app.delete(
            '/api/businesses/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_empty_business(self):
        response = self.app.delete(
            '/api/businesses/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response.status_code, 404)

    def create_business(self):
        response = self.app.post(
            '/api/businesses',
            data=json.dumps(self.new_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        return response


if __name__ == '__main__':
    unittest.main()
