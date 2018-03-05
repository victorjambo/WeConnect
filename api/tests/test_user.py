import os
import unittest
import json
from v1 import app, users


class TestUser(unittest.TestCase):
    def setUp(self):
        """Creates the app as test client
        """
        self.app = app.test_client()
        self.new_user_info = {
            "username": "victor",
            "password": "password"
        }

    def test_user_registration(self):
        """Test if new user can be registered
        """
        response = self.app.post(
            '/api/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertGreater(len(users), 0)

    def test_deplicate_user(self):
        """Test if duplicate users can be added
        """
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
        self.assertEqual(len(users), 1)

    def test_empty_fields(self):
        """Test sign up with empty fields
        """
        empty_user_info = {
            "username": "wallcare",
            "password": ""
        }
        resp = self.app.post(
            '/api/auth/register',
            data=json.dumps(empty_user_info),
            content_type='application/json'
        )

        self.assertEqual(resp.status_code, 204)

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
