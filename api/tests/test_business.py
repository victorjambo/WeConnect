import os
import unittest
import json
from v1 import app, businesses


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

    def test_business_list(self):
        """Test if can access endpoint for all businesses
        """
        response = self.app.get('/api/businesses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertGreater(len(businesses), 4)

    def test_create_business(self):
        """Test if can register new business
        """
        initial_business_count = len(businesses)
        response = self.app.post(
            '/api/businesses',
            data=json.dumps(self.new_business_info),
            content_type='application/json'
        )
        final_business_count = len(businesses)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(final_business_count - initial_business_count, 1)

    def test_read_one_business(self):
        """Test route for single business
        """
        response = self.app.get('/api/businesses/6')
        self.assertEqual(response.status_code, 200)

    def test_read_no_business(self):
        response = self.app.get('/api/businesses/60')
        self.assertEqual(response.status_code, 404)

    def test_update_business(self):
        """Test Update business info
        """
        resp = self.app.put(
            '/api/business/6',
            data=json.dumps(self.update_business_info),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 202)

    def test_delete_business(self):
        response = self.app.delete('/api/business/5')
        self.assertEqual(response.status_code, 200)

        # delete already deleted business
        response = self.app.delete('/api/business/5')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
