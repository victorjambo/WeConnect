import os
import unittest
import json
from src import app, users


class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.new_user_info = {
            "username": "victor",
            "password": "password"
        }

    def test_user_registration(self):
        response = self.app.post(
            '/api/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn(self.new_user_info, users)

    def test_deplicate_user(self):
        self.app.post(
            '/api/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        resp = self.app.post(
            '/api/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 409)

    def test_user_login(self):
        pass

    def reset_password(self):
        pass

    def test_read_all_users(self):
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_read_one_user(self):
        pass

    def test_read_user_businesses(self):
        pass


if __name__ == '__main__':
    unittest.main()
