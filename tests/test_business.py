import os
import unittest
import json
from versions import app, business_instance


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

    def test_read_all_businesses(self):
        """Test if can access endpoint for all businesses
        """
        self.create_business(self.new_business_info)
        response = self.app.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(business_instance.businesses), 0)

        output = json.loads(response.get_data(as_text=True))['businesses']
        self.assertEqual(output[0]['name'], 'Crown')

    def test_create_business(self):
        """Test if can register new business
        """
        initial_business_count = len(business_instance.businesses)
        response = self.create_business(self.new_business_info)
        final_business_count = len(business_instance.businesses)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(final_business_count - initial_business_count, 1)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'successfully created business')
        self.assertEqual(output['user'], business_instance.businesses[-1])

    def test_can_read_one_business(self):
        """Test route for single business
        """
        business_data = {
            "name": "Samsung",
            "category": "Tv",
            "location": "New york",
            "bio": "watch it again"
        }
        self.create_business(business_data)
        response = self.app.get('/api/v1/business/1')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['business']
        self.assertEqual(output['name'], business_data['name'])

    def test_read_no_business(self):
        """Test 404 not found on business not existing
        """
        response = self.app.get('/api/v1/business/60')
        self.assertEqual(response.status_code, 404)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Business Not Found')

    def test_cannot_update_business(self):
        """Test Update business info for non existing business
        """
        resp = self.app.put(
            '/api/v1/business/45',
            data=json.dumps(self.update_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_business(self):
        initial = len(business_instance.businesses)
        response = self.app.delete(
            '/api/v1/business/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        final = len(business_instance.businesses)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(initial - final, 1)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'Business Deleted')

    def test_delete_empty_business(self):
        response = self.app.delete(
            '/api/v1/business/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response.status_code, 404)

    def create_business(self, business_data):
        response = self.app.post(
            '/api/v1/businesses',
            data=json.dumps(business_data),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        return response


if __name__ == '__main__':
    unittest.main()
