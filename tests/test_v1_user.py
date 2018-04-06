import unittest
import json
from versions import app, user_instance, business_instance


class TestUser(unittest.TestCase):
    def setUp(self):
        """Creates the app as test client
        """
        self.app = app.test_client()
        self.new_user_info = {
            "username": "robert",
            "email": "victor.mutai@students.jkuat.ac.ke",
            "password": "password1234"
        }
        self.user_login_info = {
            "username": "robert",
            "password": "password1234"
        }
        self.new_password = {
            "old_password": "password1234",
            "password": "wallcare12345"
        }
        self.with_new_pass = {
            "username": "robert",
            "password": "wallcare12345"
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
            '/api/v1/auth/register',
            data=json.dumps(empty_user_info),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Provide email, username & password')

        self.assertEqual(response.status_code, 400)

    def test_user_registration(self):
        """Test if new user can be registered
        """
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        self.assertGreater(len(user_instance.users), 0)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(
            output['success'],
            'User created, Check mail box to activate account'
        )
        self.assertEqual(output['user'], user_instance.users[-1]['username'])

    def test_user_registration_dup_username(self):
        """Test if duplicate users can be added
        """
        self.register_user()
        response = self.register_user()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(len(user_instance.users), 1)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Username has already been taken')

    def test_user_registration_dup_email(self):
        """Test create user with same email as existing
        """
        self.register_user()
        user_info = {
            "username": "victor",
            "email": "victor.mutai@students.jkuat.ac.ke",
            "password": "password1234"
        }
        response = self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(user_info),
            content_type='application/json'
        )

        self.assertEqual(len(user_instance.users), 1)
        self.assertEqual(response.status_code, 409)
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Email has already been taken')

    def test_user_registration_with_weak_password(self):
        """test week passwords
        """
        week_password = {
            'username': 'vivian',
            'email': 'victorjambo@live.com',
            'password': '123'
        }
        response = self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(week_password),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Please provide strong password')

    def test_user_registration_with_bad_email(self):
        """test week passwords
        """
        with_bad_email = {
            'username': 'vivian',
            'email': 'some@gmail',
            'password': 'password1234'
        }
        response = self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(with_bad_email),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Please provide valid email')

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
            '/api/v1/auth/login',
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
            'password': 'passwords1234'
        }
        response = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(bad_params),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Incorrect username')

    def test_cannot_login(self):
        """Test if user cannot login
        """
        bad_params = {
            'username': 'robert',
            'password': 'password2586'
        }
        self.register_user()
        response = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(bad_params),
            content_type='application/json'
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Cannot Login wrong password')

    def test_reset_password(self):
        """Test user can reset password
        and login with new password
        """
        self.register_user()
        self.login_user()
        response1 = self.app.put(
            '/api/v1/auth/reset-password',
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
            '/api/v1/auth/login',
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
            '/api/v1/auth/login',
            data=json.dumps(self.with_new_pass),
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(response.status_code, 401)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Incorrect username')

    def test_reset_pass_with_no_token(self):
        """Send reset password with no token in header
        """
        self.register_user()
        self.login_user()
        response = self.app.put(
            '/api/v1/auth/reset-password',
            data=json.dumps(self.new_password),
            headers={
                "content-type": "application/json"
            }
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Missing token. Please register or login')

    def test_logout(self):
        """Test user logout
        """
        self.register_user()
        self.login_user()
        response = self.app.delete(
            '/api/v1/auth/logout',
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
            '/api/v1/auth/logout',
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
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['users']
        self.assertEqual(output[0]['username'], self.new_user_info['username'])

    def test_read_one_user(self):
        """Test endpoint for one user
        """
        self.register_user()
        self.login_user()
        response = self.app.get('/api/v1/user/1')
        self.assertEqual(response.status_code, 200)

    def test_not_found_user(self):
        """Test endpoint if user doesn't exist
        """
        response = self.app.get('/api/v1/user/15')
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(
            output,
            "user does not exist"
        )

    def test_read_user_businesses(self):
        """Test all business owned by user
        """
        self.register_user()
        self.login_user()
        self.create_business()
        response = self.app.get('/api/v1/user/1/businesses')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['user']
        self.assertEqual(output[-1]['name'], 'Crown')

    def test_not_found_user_businesses(self):
        """Test all business owned by user
        If user doesn't exist
        """
        self.register_user()
        self.login_user()
        response = self.app.get('/api/v1/user/100/businesses')
        self.assertEqual(response.status_code, 404)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'user does not own a business')

    def test_user_does_not_exist(self):
        """test user does not exist
        """
        # self.register_user()
        # self.login_user()
        response = self.app.get('/api/v1/user/112')
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'user does not exist')

    def register_user(self):
        response = self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        return response

    def login_user(self):
        response = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(self.user_login_info),
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
            '/api/v1/businesses',
            data=json.dumps(new_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        return response

    def tearDown(self):
        """Clear list"""
        user_instance.users.clear()
        business_instance.businesses.clear()


if __name__ == '__main__':
    unittest.main()
