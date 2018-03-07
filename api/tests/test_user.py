import os
import unittest
import json
from v1 import app, user_instance


class TestUser(unittest.TestCase):
    def setUp(self):
        """Creates the app as test client
        """
        self.app = app.test_client()
        self.new_user_info = {
            "username": "robert",
            "password": "password"
        }
        self.new_password = {
            "password": "12345"
        }
        self.token = ''

    def test_signup_with_empty_fields(self):
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

    def test_user_registration(self):
        """Test if new user can be registered
        """
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertGreater(len(user_instance.users), 0)

    def test_user_registration_duplication(self):
        """Test if duplicate users can be added
        """
        self.register_user()
        resp = self.register_user()
        self.assertEqual(resp.status_code, 409)
        self.assertEqual(len(user_instance.users), 1)

    def test_successful_login(self):
        """ Test if user can login successfully
        """
        self.register_user()
        resp = self.login_user()
        self.assertEqual(resp.status_code, 200)

    def reset_password(self):
        """Test user can reset password
        and login with new password
        """
        self.register_user()
        self.login_user()
        resp = self.app.put(
            '/api/auth/reset-password',
            data=json.dumps(self.new_password),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.app.post(
            '/api/auth/login',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

    def test_logout(self):
        """Test user logout
        """
        self.register_user()
        self.login_user()
        resp = self.app.delete(
            '/api/auth/logout',
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

    def test_read_all_users(self):
        """Test Get all users route
        """
        resp = self.app.get('/api/users')
        self.assertEqual(resp.status_code, 200)

    def test_read_one_user(self):
        """Test endpoint for one user
        """
        self.register_user()
        self.login_user()
        resp = self.app.get('/api/user/1')
        self.assertEqual(resp.status_code, 200)

    def test_not_found_user(self):
        """Test endpoint if user doesn't exist
        """
        resp = self.app.get('/api/user/12')
        self.assertEqual(resp.status_code, 404)

    def test_read_user_businesses(self):
        """Test all business owned by user
        """
        resp = self.app.get('/api/user/1/businesses')
        self.assertEqual(resp.status_code, 200)

    def test_not_found_user_businesses(self):
        """Test all business owned by user
        If user doesn't exist
        """
        resp = self.app.get('/api/user/13/businesses')
        self.assertEqual(resp.status_code, 204)

    def register_user(self):
        response = self.app.post(
            '/api/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        return response

    def login_user(self):
        resp = self.app.post(
            '/api/auth/login',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        return resp

    def tearDown(self):
        """"""
        user_instance.users.clear()


if __name__ == '__main__':
    unittest.main()
