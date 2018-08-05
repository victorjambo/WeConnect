import unittest
import json
from versions import app
from versions.v2.models import User, db, Notification, Business, Review


class TestNotification(unittest.TestCase):
    def setUp(self):
        """Creates the app as test client
        """
        self.app = app.test_client()
        self.new_user_login = {
            'username': 'victor',
            'password': 'password1234'
        }
        self.new_user_info = {
            'username': 'victor',
            'fullname': 'victor jambo',
            'email': 'victor.mutai@gmail.com',
            'password': 'password1234'
        }

    def test_get_notification(self):
        """Test get notification
        """
        self.register()
        token = json.loads(self.login().get_data(as_text=True))['token']

        response = self.app.get(
            '/api/v2/notifications',
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response.status_code, 200)
        warning = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual('user has no notifications', warning)

    def register(self):
        return self.app.post(
            '/api/v2/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        
    def login(self):
        return self.app.post(
            '/api/v2/auth/login',
            data=json.dumps(self.new_user_login),
            content_type='application/json'
        )
        
    def tearDown(self):
        """Clean-up db"""
        db.session.query(Notification).delete()
        db.session.query(Review).delete()
        db.session.query(Business).delete()
        db.session.query(User).delete()
        db.session.commit()

if __name__ == '__main__':
    unittest.main()
