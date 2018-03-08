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
        self.with_new_pass = {
            "username": "robert",
            "password": "12345"
        }
        self.token = {}

    def test_signup_with_empty_fields(self):
        """Test sign up with empty fields
        """
        empty_user_info = {
            "username": "wallcare",
            "password": ""
        }
        response = self.app.post(
            '/api/auth/register',
            data=json.dumps(empty_user_info),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Cannot create user without password')

        self.assertEqual(response.status_code, 400)

    def test_user_registration(self):
        """Test if new user can be registered
        """
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertGreater(len(user_instance.users), 0)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'Successfully created user')
        self.assertEqual(output['user'], user_instance.users[-1]['username'])

    def test_user_registration_duplication(self):
        """Test if duplicate users can be added
        """
        self.register_user()
        response = self.register_user()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(len(user_instance.users), 1)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Username has already been taken')

    def test_user_registration_with_weak_password(self):
        """test week passwords
        """
        week_password = {
            'username': 'vivian',
            'password': '123'
        }
        response = self.app.post(
            '/api/auth/register',
            data=json.dumps(week_password),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Please provide strong password')

    def test_successful_login(self):
        """ Test if user can login successfully
        """
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['success']
        self.assertEqual(output, 'Login success')

    def test_login_with_bad_params(self):
        """Test if user can login with bad params
        """
        bad_params = {
            'username': 'victo'
        }
        response = self.app.post(
            '/api/auth/login',
            data=json.dumps(bad_params),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Provide username & password')

    def test_login_with_wrong_username(self):
        """Test if user can login with bad username
        or user that does not exist
        """
        bad_params = {
            'username': 'someone',
            'password': 'passwords'
        }
        response = self.app.post(
            '/api/auth/login',
            data=json.dumps(bad_params),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Incorrect username')

    def test_reset_password(self):
        """Test user can reset password
        and login with new password
        """
        self.register_user()
        self.login_user()
        response1 = self.app.put(
            '/api/auth/reset-password',
            data=json.dumps(self.new_password),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response1.status_code, 200)

        output = json.loads(response1.get_data(as_text=True))['success']
        self.assertEqual(output, 'password updated')

        response2 = self.app.post(
            '/api/auth/login',
            data=json.dumps(self.with_new_pass),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response2.status_code, 200)

        output = json.loads(response2.get_data(as_text=True))['success']
        self.assertEqual(output, 'Login success')

    def test_reset_password_login_wrong_username(self):
        """Bad login info"""
        response = self.app.post(
            '/api/auth/login',
            data=json.dumps(self.with_new_pass),
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(response.status_code, 401)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Incorrect username')

    def test_logout(self):
        """Test user logout
        """
        self.register_user()
        self.login_user()
        response = self.app.delete(
            '/api/auth/logout',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['success']
        self.assertEqual(output, 'logged out')

        # logout again
        response2 = self.app.delete(
            '/api/auth/logout',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response2.status_code, 404)

        output = json.loads(response2.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Already logged out')

    def test_read_all_users(self):
        """Test Get all users route
        """
        self.register_user()
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['users']
        self.assertEqual(output[0]['username'], self.new_user_info['username'])

    def test_read_one_user(self):
        """Test endpoint for one user
        """
        self.register_user()
        self.login_user()
        resp = self.app.get(
            '/api/user/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(resp.status_code, 200)

    def test_not_found_user(self):
        """Test endpoint if user doesn't exist
        """
        resp = self.app.get('/api/user/15')
        self.assertEqual(resp.data, b'{\n  "warning": "token missing"\n}\n')

    def test_read_user_businesses(self):
        """Test all business owned by user
        """
        self.register_user()
        self.create_business()
        response = self.app.get('/api/user/1/businesses')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['user']
        self.assertEqual(output[0]['name'], 'Crown')

    def test_not_found_user_businesses(self):
        """Test all business owned by user
        If user doesn't exist
        """
        self.register_user()
        response = self.app.get('/api/user/100/businesses')
        self.assertEqual(response.status_code, 404)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'user does not own a business')

    def register_user(self):
        response = self.app.post(
            '/api/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        return response

    def login_user(self):
        response = self.app.post(
            '/api/auth/login',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        self.token = json.loads(response.get_data(as_text=True))['token']
        return response

    def create_business(self):
        new_business_info = {
            "name": "Crown",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }
        response = self.app.post(
            '/api/businesses',
            data=json.dumps(new_business_info),
            content_type='application/json'
        )
        return response

    def tearDown(self):
        """Clear user list"""
        user_instance.users.clear()


if __name__ == '__main__':
    unittest.main()
