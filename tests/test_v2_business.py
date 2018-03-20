import unittest
import json
from versions import app
from versions.v2.models import User, db, Business


class TestBusinessV2(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.Testing')
        self.app = app.test_client()
        self.new_business_info = {
            "name": "Crown",
            "logo": "url",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }
        self.update_business_info = {
            "name": "Crown paints",
            "logo": "url",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }
        self.new_user_info = {
            "username": "robert",
            "email": "victor.mutai@jkuat.comm",
            "password": "password1234"
        }
        self.user_login_info = {
            "username": "robert",
            "password": "password1234"
        }

    def test_read_all_businesses(self):
        """Test if can access endpoint for all businesses
        """
        self.register_business()
        response = self.app.get('/api/v2/businesses/')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.get_data(as_text=True))['businesses']
        self.assertEqual(output[0]['name'], self.new_business_info['name'])

    def test_read_if_no_businesses(self):
        """Test what happens when no businesses
        """
        response = self.app.get('/api/v2/businesses/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('No Businesses, create one first', str(response.data))

    def test_create_business(self):
        """Test if can register new business
        """
        response = self.register_business()
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'successfully created business')
        exists = db.session.query(
            db.exists().where(Business.name == output['business']['name'])
        ).scalar()
        self.assertTrue(exists)

    def test_validate_create_business_name(self):
        """Create business with bad name format
        """
        business_data = {
            "name": "    ",
            "category": "Tv",
            "location": "New york",
            "bio": "watch it again"
        }
        self.register_user()
        response = self.app.post(
            '/api/v2/businesses',
            data=json.dumps(business_data),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Please provide name with more characters')

    def test_create_business_if_name_taken(self):
        """Test create business if name is taken
        """
        self.register_business()
        response = self.register_business()
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(
            output,
            'Business name {} already taken'.format(
                self.new_business_info['name']))

    def test_can_read_one_business(self):
        """Test route for single business
        """
        new_business = self.register_business()
        business_id = json.loads(
            new_business.get_data(as_text=True))['business']['id']

        response = self.app.get('/api/v2/businesses/{}'.format(business_id))
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.get_data(as_text=True))['business']
        self.assertEqual(output['id'], business_id)

    def test_read_no_business(self):
        """Test 404 not found on business not existing
        """
        response = self.app.get('/api/v2/businesses/6000')
        self.assertEqual(response.status_code, 404)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Business Not Found')

    def test_update_business(self):
        """Test if user can update business
        """
        new_business = self.register_business()
        business_id = json.loads(
            new_business.get_data(as_text=True))['business']['id']

        response = self.app.put(
            '/api/v2/businesses/{}'.format(business_id),
            data=json.dumps(self.update_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertIn('successfully updated', str(response.data))
        _business = json.loads(response.get_data(as_text=True))
        exists = db.session.query(
            db.exists().where(Business.name == _business['business']['name']))
        self.assertTrue(exists)

    def test_unsuccesful_update(self):
        """Test update if business doesn't exist"""
        self.register_user()
        response = self.app.put(
            '/api/v2/businesses/6000',
            data=json.dumps(self.update_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertIn('Business Not Found', str(response.data))
        self.assertEqual(response.status_code, 404)

    def test_delete_business_not_owner(self):
        """Test delete not your business
        """
        new_user = {
            "username": "hotpoint",
            "email": "victor.mutai@nbo.samadc.org",
            "password": "password1234"
        }
        new_user_login = {
            "username": "hotpoint",
            "password": "password1234"
        }
        self.app.post(
            '/api/v2/auth/register',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        response_login = self.app.post(
            '/api/v2/auth/login',
            data=json.dumps(new_user_login),
            content_type='application/json'
        )
        token = json.loads(response_login.get_data(as_text=True))['token']
        new_business = self.register_business()
        business_id = json.loads(
            new_business.get_data(as_text=True))['business']['id']

        response = self.app.delete(
            '/api/v2/businesses/{}'.format(business_id),
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response.status_code, 401)

        self.assertIn('Not Allowed, you are not owner', str(response.data))

    def test_delete_business(self):
        """Test if actually deleted business
        """
        new_business = self.register_business()
        business_id = json.loads(
            new_business.get_data(as_text=True))['business']['id']

        response = self.app.delete(
            '/api/v2/businesses/{}'.format(business_id),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Business Deleted', str(response.data))

    def test_delete_empty_business(self):
        """Test delete already deleted business
        """
        self.register_user()
        response = self.app.delete(
            '/api/v2/businesses/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('Business Not Found', str(response.data))

    def register_user(self):
        return self.app.post(
            '/api/v2/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )

    def login(self):
        return self.app.post(
            '/api/v2/auth/login',
            data=json.dumps(self.user_login_info),
            content_type='application/json'
        )

    def token(self):
        response = self.app.post(
            '/api/v2/auth/login',
            data=json.dumps(self.user_login_info),
            content_type='application/json')
        return json.loads(response.get_data(as_text=True))['token']

    def register_business(self):
        self.register_user()
        return self.app.post(
            '/api/v2/businesses',
            data=json.dumps(self.new_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()})

    def tearDown(self):
        """Clean-up db"""
        db.session.query(Business).delete()
        db.session.query(User).delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
