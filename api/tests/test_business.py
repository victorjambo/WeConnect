import os
import unittest
import json
from v1 import app, businesses


class TestUser(unittest.TestCase):
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
        response = self.app.get('/api/businesses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_create_business(self):
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
        assert self.new_business_info in businesses

    def test_read_one_business(self):
        response = self.app.get('/api/businesses/6')
        self.assertEqual(response.status_code, 200)
        assert response in businesses
        self.assertEqual(businesses[-1], self.new_business_info)

    def test_update_business(self):
        self.app.put(
            '/api/business/6',
            data=json.dumps(self.update_business_info),
            content_type='application/json'
        )
        self.assertEqual(businesses[-1], self.new_business_info)

    def test_delete_business(self):
        response = self.app.delete('/api/business/6')
        self.assertEqual(response.status_code, 200)

        # delete already deleted busines
        response = self.app.delete('/api/business/6')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
