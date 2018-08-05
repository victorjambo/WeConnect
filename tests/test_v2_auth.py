import unittest
import json
from versions import app
from versions.v2.models import User, db
from passlib.hash import sha256_crypt


class TestAuth(unittest.TestCase):
    def setUp(self):
        """Creates the app as test client
        """
        app.config.from_object('config.Testing')
        self.app_client = app.test_client()
        self.new_user_info = {
            'username': 'victorjambo',
            'fullname': 'victor jambo',
            'email': 'victor.mutai@gmail.com',
            'password': 'password1234'
        }
        self.new_user_login = {
            'username': 'victorjambo',
            'password': 'password1234'
        }
        self.new_password = {
            "old_password": "password1234",
            "password": "wallcare12345"
        }

    def test_user_registration(self):
        """Test user can be registered
        """
        response = self.register()
        exists = db.session.query(
            db.exists().where(User.username == self.new_user_info['username'])
        ).scalar()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(exists)

    def test_unsuccesfull_user_registration(self):
        """Test when user is no registered successfully
        1. test fail when all fields are not provided
        2. test fail when username is taken
        3. test fail when email is taken
        4. test fail on username validation
        5. test fail on email validation
        6. test fail on password validation
        """
        self.register()
        # 1. test fail when all fields are not provided
        auth1 = {
            'username': 'victor1',
            'password': 'password1234'
        }
        response1 = self.app_client.post(
            '/api/v2/auth/register',
            data=json.dumps(auth1),
            content_type='application/json'
        )
        exists1 = db.session.query(
            db.exists().where(User.username == auth1['username'])
        ).scalar()
        self.assertEqual(response1.status_code, 400)
        self.assertFalse(exists1)
        self.assertIn(
            'All Fields Required',
            str(response1.data))

        # 2. test fail when username is taken
        auth2 = {
            'username': 'victorjambo',
            'fullname': 'victor jambo',
            'email': 'victor2.mutai@gmail.com',
            'password': 'password1234'
        }
        response2 = self.app_client.post(
            '/api/v2/auth/register',
            data=json.dumps(auth2),
            content_type='application/json'
        )
        exists2 = db.session.query(
            db.exists().where(User.email == auth2['email'])
        ).scalar()
        self.assertEqual(response2.status_code, 409)
        self.assertFalse(exists2)
        self.assertIn(
            'Username has already been taken',
            str(response2.data))

        # 3. test fail when email is taken
        auth3 = {
            'username': 'victor3',
            'fullname': 'vitor muts',
            'email': 'victor.mutai@gmail.com',
            'password': 'password1234'
        }
        response3 = self.app_client.post(
            '/api/v2/auth/register',
            data=json.dumps(auth3),
            content_type='application/json'
        )
        exists3 = db.session.query(
            db.exists().where(User.username == auth3['username'])
        ).scalar()
        self.assertEqual(response3.status_code, 409)
        self.assertFalse(exists3)
        self.assertIn('Email has already been taken', str(response3.data))

        # 4. test fail on username validation
        auth4 = {
            'username': 'a',
            'fullname': 'victor jambo',
            'email': 'victor4.mutai@gmail.com',
            'password': 'password1234'
        }
        response4 = self.app_client.post(
            '/api/v2/auth/register',
            data=json.dumps(auth4),
            content_type='application/json'
        )
        exists4 = db.session.query(
            db.exists().where(User.username == auth4['username'])
        ).scalar()
        self.assertEqual(response4.status_code, 409)
        self.assertFalse(exists4)
        self.assertIn(
            'Invalid username',
            str(response4.data))

        # 5. test fail on email validation
        auth5 = {
            'username': 'abcd',
            'fullname': 'victor jambo',
            'email': 'victor.mutai@',
            'password': 'password1235'
        }
        response5 = self.app_client.post(
            '/api/v2/auth/register',
            data=json.dumps(auth5),
            content_type='application/json'
        )
        exists5 = db.session.query(
            db.exists().where(User.username == auth5['username'])
        ).scalar()
        self.assertEqual(response5.status_code, 409)
        self.assertFalse(exists5)
        self.assertIn(
            'Invalid email',
            str(response5.data))

        # 6. test fail on password validation
        auth6 = {
            'username': 'abcd',
            'fullname': 'victor jambo',
            'email': 'victor6.mutai@gmail.com',
            'password': 'password'
        }
        response6 = self.app_client.post(
            '/api/v2/auth/register',
            data=json.dumps(auth6),
            content_type='application/json'
        )
        exists6 = db.session.query(
            db.exists().where(User.username == auth6['username'])
        ).scalar()
        self.assertEqual(response6.status_code, 409)
        self.assertFalse(exists6)
        self.assertIn(
            'Provide strong password',
            str(response6.data))

    def test_login(self):
        """Test Login user"""
        new_user = self.register()
        exists = db.session.query(
            db.exists().where(User.username == self.new_user_info['username'])
        ).scalar()
        self.assertEqual(new_user.status_code, 200)
        self.assertTrue(exists)

        new_login = self.login()
        self.assertEqual(new_login.status_code, 200)
        self.assertIn('Login success', str(new_login.data))

    def test_unsuccesfull_login(self):
        """Test unsuccesfull login
        1. test validation
        2. test non-existant user
        3. test wrong password
        """
        self.register()

        # 1. test validation
        login_1 = {'username': 'victor'}
        new_login_1 = self.app_client.post(
            '/api/v2/auth/login',
            data=json.dumps(login_1),
            content_type='application/json'
        )
        self.assertEqual(new_login_1.status_code, 400)
        self.assertIn('Provide username & password', str(new_login_1.data))

        # 2. test non-existant user
        login_2 = {
            'username': 'someoneelse',
            'password': 'password1234'}
        new_login_2 = self.app_client.post(
            '/api/v2/auth/login',
            data=json.dumps(login_2),
            content_type='application/json'
        )
        self.assertEqual(new_login_2.status_code, 401)
        self.assertIn(
            '{} does not exist'.format(login_2['username']),
            str(new_login_2.data))

        # 3. test wrong password
        login_3 = {
            'username': 'victorjambo',
            'password': 'password'}
        new_login_3 = self.app_client.post(
            '/api/v2/auth/login',
            data=json.dumps(login_3),
            content_type='application/json'
        )
        self.assertEqual(new_login_3.status_code, 401)
        self.assertIn(
            'Cannot Login wrong password',
            str(new_login_3.data))

    def test_reset_password(self):
        """Test reset password"""
        self.register()
        initial_password = User.query.filter_by(
            username=self.new_user_info['username']).first().password
        token = json.loads(self.login().get_data(as_text=True))['token']
        response = self.app_client.put(
            '/api/v2/auth/reset-password',
            data=json.dumps(self.new_password),
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('password updated', str(response.data))

        final_password = User.query.filter_by(
            username=self.new_user_login['username']).first().password
        self.assertIsNot(final_password, initial_password)
        self.assertFalse(sha256_crypt.verify(final_password, initial_password))

    def test_unsuccesfull_reset_password(self):
        """Test user unsuccessful reset password
        1. not logged in
        2. passwords not matching
        """
        self.register()
        token = json.loads(self.login().get_data(as_text=True))['token']

        # 1. not logged in
        response1 = self.app_client.put(
            '/api/v2/auth/reset-password',
            data=json.dumps(self.new_password),
            content_type='application/json'
        )
        self.assertIn(
            'Missing token. Please register or login', str(response1.data))

        # 2. passwords not matching
        new_password = {
            'old_password': 'wrong1234',
            'password': 'wrong1234'
        }
        response2 = self.app_client.put(
            '/api/v2/auth/reset-password',
            data=json.dumps(new_password),
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertIn('old password does not match', str(response2.data))

    def test_logout(self):
        """Test logout
        """
        self.register()
        token = json.loads(self.login().get_data(as_text=True))['token']

        response = self.app_client.delete(
            '/api/v2/auth/logout',
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['success']
        self.assertEqual(output, 'logged out')

        # logout again
        response2 = self.app_client.delete(
            '/api/v2/auth/logout',
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response2.status_code, 401)

        output = json.loads(response2.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Login again')

    def test_forgot_password(self):
        """Test when user has forgotten password"""
        self.register()
        email = {'email': 'victor.mutai@gmail.com'}
        response = self.app_client.post(
            '/api/v2/auth/forgot-password',
            data=json.dumps(email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email has been sent with new password', str(response.data))

    def test_unsuccessful_forgot_password(self):
        """Test email not found at forgot password"""
        email = {'email': 'vic_mutai@gmail.com'}
        response = self.app_client.post(
            '/api/v2/auth/forgot-password',
            data=json.dumps(email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
        self.assertIn('No user exists with that email', str(response.data))

    def test_verify_account(self):
        """Test activation url"""
        self.register()
        response = self.app_client.get(
            '/api/v2/auth/verify?key=123&name=victorjambo',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 301)

    def register(self):
        return self.app_client.post(
            '/api/v2/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )

    def login(self):
        return self.app_client.post(
            '/api/v2/auth/login',
            data=json.dumps(self.new_user_login),
            content_type='application/json'
        )

    def tearDown(self):
        """Clean-up db"""
        db.session.query(User).delete()
        db.session.commit()
