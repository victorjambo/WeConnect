import unittest
import json
from versions import app, business_instance, user_instance


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
        self.new_user_info = {
            "username": "robert",
            "email": "victor.mutai@students.jkuat.ac.ke",
            "password": "password1234"
        }
        self.user_login_info = {
            "username": "robert",
            "password": "password1234"
        }
        self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(self.new_user_info),
            content_type='application/json'
        )
        response = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(self.user_login_info),
            content_type='application/json'
        )
        self.token = json.loads(response.get_data(as_text=True))['token']

    def test_read_all_businesses(self):
        """Test if can access endpoint for all businesses
        """
        self.create_business(self.new_business_info)
        response = self.app.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(business_instance.businesses), 0)

        output = json.loads(response.get_data(as_text=True))['businesses']
        self.assertEqual(output[0]['name'], 'Crown')

    def test_read_if_no_businesses(self):
        """Test what happens when no businesses
        """
        business_instance.businesses.clear()
        self.assertEqual(len(business_instance.businesses), 0)
        response = self.app.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'No Businesses')

    def test_create_business(self):
        """Test if can register new business
        """
        initial_business_count = len(business_instance.businesses)
        response = self.create_business(self.new_business_info)
        final_business_count = len(business_instance.businesses)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(final_business_count - initial_business_count, 1)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'successfully created business')
        self.assertEqual(output['business'], business_instance.businesses[-1])

    def test_validate_create_business_name(self):
        """Create business with bad name format
        """
        business_data = {
            "name": "    ",
            "category": "Tv",
            "location": "New york",
            "bio": "watch it again"
        }

        response = self.create_business(business_data)
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Please provide name with more characters')

    def test_create_business_if_name_taken(self):
        """Test create business if name is taken
        """
        new_business_info = {
            "name": "Crown",
            "category": "Technology",
            "location": "Eldoret",
            "bio": "white stays white"
        }
        self.create_business(self.new_business_info)
        response = self.create_business(new_business_info)
        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(
            output,
            'Business name {} already taken'.format(
                self.new_business_info['name']
            )
        )

    def test_can_read_one_business(self):
        """Test route for single business
        """
        business_data = {
            "name": "Samsung",
            "category": "Tv",
            "location": "New york",
            "bio": "watch it again"
        }
        self.create_business(business_data)
        response = self.app.get('/api/v1/businesses/1')
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['business']
        self.assertEqual(output['name'], business_data['name'])

    def test_read_no_business(self):
        """Test 404 not found on business not existing
        """
        response = self.app.get('/api/v1/businesses/60')
        self.assertEqual(response.status_code, 404)

        output = json.loads(response.get_data(as_text=True))['warning']
        self.assertEqual(output, 'Business Not Found')

    def test_update_business(self):
        """Test if user can update business
        """
        business_data = {
            "name": "Andela Kenya",
            "category": "Tv",
            "location": "New york",
            "bio": "watch it again"
        }
        update_business_data = {
            "name": "",
            "category": "Technology",
            "location": "",
            "bio": ""
        }
        self.create_business(business_data)
        response = self.app.put(
            '/api/v1/businesses/1',
            data=json.dumps(update_business_data),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'successfully updated')
        self.assertEqual(
            output['business']['category'],
            update_business_data['category']
        )

    def test_cannot_update_business(self):
        """Test Update business info for non existing business
        1. Business not found
        2. Not Allowed. update by different user
        3. Business name that fails regex
        4. If name key is not provided
        5. If category key is not provided
        6. If location key is not provided
        7. If bio key is not provided
        """
        self.create_business(self.new_business_info)

        # 1. Business not found
        response1 = self.app.put(
            '/api/v1/businesses/45',
            data=json.dumps(self.update_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response1.status_code, 404)
        output1 = json.loads(response1.get_data(as_text=True))['warning']
        self.assertEqual(output1, 'Business Not Found')

        # 2. Not Allowed. update by different user
        new_user = {
            "username": "hotpoint",
            "email": "victor.mutai@nbo.samadc.org",
            "password": "password1234"
        }
        new_user_login = {
            "username": "hotpoint",
            "password": "password1234"
        }
        update_business_data = {
            "name": "",
            "category": "Technology",
            "location": "",
            "bio": ""
        }
        self.app.post(
            '/api/v1/auth/register',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        response2_login = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(new_user_login),
            content_type='application/json'
        )
        token = json.loads(response2_login.get_data(as_text=True))['token']
        response2 = self.app.put(
            '/api/v1/businesses/1',
            data=json.dumps(update_business_data),
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response2.status_code, 401)
        output2 = json.loads(response2.get_data(as_text=True))['warning']
        self.assertEqual(output2, 'Not Allowed')
        self.assertIsNot(
            business_instance.businesses[0]['category'],
            update_business_data['category']
        )

        # 3. Business name that fails regex
        update_business_data3 = {
            "name": "123",
            "category": "",
            "location": "",
            "bio": ""
        }
        response3 = self.app.put(
            '/api/v1/businesses/1',
            data=json.dumps(update_business_data3),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        output = json.loads(response3.get_data(as_text=True))
        self.assertEqual(
            output['warning'],
            'Please provide name with more characters')
        self.assertIsNot(
            business_instance.businesses[0]['name'],
            update_business_data3['name']
        )

        # 4. If name key is not provided
        update_business_data4 = {
            "category": "",
            "location": "Eldoret",
            "bio": ""
        }
        response4 = self.app.put(
            '/api/v1/businesses/1',
            data=json.dumps(update_business_data4),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        output = json.loads(response4.get_data(as_text=True))
        self.assertEqual(
            output['warning'],
            'provide business name, leave blank for no update'
        )
        self.assertIsNot(
            business_instance.businesses[0]['location'],
            update_business_data4['location']
        )

        # 5. If category key is not provided
        update_business_data5 = {
            "name": "",
            "location": "Eldoret",
            "bio": ""
        }
        response5 = self.app.put(
            '/api/v1/businesses/1',
            data=json.dumps(update_business_data5),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        output = json.loads(response5.get_data(as_text=True))
        self.assertEqual(
            output['warning'],
            'provide category, leave blank for no update'
        )
        self.assertIsNot(
            business_instance.businesses[0]['location'],
            update_business_data5['location']
        )

        # 6. If location key is not provided
        update_business_data6 = {
            "name": "",
            "category": "Firebase",
            "bio": ""
        }
        response6 = self.app.put(
            '/api/v1/businesses/1',
            data=json.dumps(update_business_data6),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        output = json.loads(response6.get_data(as_text=True))
        self.assertEqual(
            output['warning'],
            'provide location, leave blank for no update'
        )
        self.assertIsNot(
            business_instance.businesses[0]['category'],
            update_business_data6['category'])

        # 7. If bio key is not provided
        update_business_data7 = {
            "name": "",
            "location": "",
            "category": "Firebase"
        }
        response7 = self.app.put(
            '/api/v1/businesses/1',
            data=json.dumps(update_business_data7),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        output = json.loads(response7.get_data(as_text=True))
        self.assertEqual(
            output['warning'],
            'provide bio, leave blank for no update'
        )
        self.assertIsNot(
            business_instance.businesses[0]['category'],
            update_business_data7['category']
        )

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
            '/api/v1/auth/register',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        response_login = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(new_user_login),
            content_type='application/json'
        )
        token = json.loads(response_login.get_data(as_text=True))['token']
        self.create_business(self.new_business_info)
        response = self.app.delete(
            '/api/v1/businesses/1',
            headers={
                "content-type": "application/json",
                "x-access-token": token
            }
        )
        self.assertEqual(response.status_code, 401)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['warning'], 'Not Allowed, Contact owner')

    def test_delete_business(self):
        """Test if actually deleted business
        """
        self.create_business(self.new_business_info)
        initial = len(business_instance.businesses)
        response = self.app.delete(
            '/api/v1/businesses/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        final = len(business_instance.businesses)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(initial - final, 1)

        output = json.loads(response.get_data(as_text=True))
        self.assertEqual(output['success'], 'Business Deleted')

    def test_delete_empty_business(self):
        """Test delete already deleted business
        """
        response = self.app.delete(
            '/api/v1/businesses/1',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token
            }
        )
        self.assertEqual(response.status_code, 404)

    def create_business(self, business_data):
        response = self.app.post(
            '/api/v1/businesses',
            data=json.dumps(business_data),
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
