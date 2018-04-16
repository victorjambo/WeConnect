import json
import unittest
from versions import app
from versions.v2.models import User, db, Business, Review


class TestReviewV2(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.Testing')
        self.app = app.test_client()
        self.new_review = {
            "title": "Friday 13th",
            "desc": "Lorem ipsum dolor sit amet consectetur adip elit."
        }
        self.new_user_info = {
            "username": "oliver",
            "fullname": "oliver mutai",
            "email": "oliver.mutai@maseno.com",
            "password": "password1234"
        }
        self.user_login_info = {
            "username": "oliver",
            "password": "password1234"
        }
        self.new_business_info = {
            "name": "Crown paints",
            "logo": "url",
            "category": "Construction",
            "location": "NBO",
            "bio": "if you like it crown it"
        }

    def test_create_review(self):
        """Create new review for a business
        """
        response = self.register_review()
        self.assertEqual(response.status_code, 201)
        self.assertIn('successfully created review', str(response.data))
        _review = json.loads(response.get_data(as_text=True))
        exists = db.session.query(
            db.exists().where(Review.title == _review['review']['title']))
        self.assertTrue(exists)

    def test_read_reviews(self):
        """Get reviews for business
        """
        new_business = self.register_business()
        business_id = json.loads(
            new_business.get_data(as_text=True))['business']['id']

        new_review = self.app.post(
            '/api/v2/businesses/{}/reviews'.format(business_id),
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()})

        review_id = json.loads(
            new_review.get_data(as_text=True))['review']['id']

        resp = self.app.get(
            '/api/v2/businesses/{}/reviews'.format(business_id))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            review_id,
            json.loads(resp.get_data(as_text=True))['reviews'][0]['id'])

        response = self.app.get(
            '/api/v2/businesses/reviews',
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )
        self.assertEqual(response.status_code, 200)

        output = json.loads(response.get_data(as_text=True))['Reviews']
        self.assertEqual(output[0]['title'], self.new_review['title'])

    def test_delete_review(self):
        """Test deleting business twice
        """
        new_business = self.register_business()
        business_id = json.loads(
            new_business.get_data(as_text=True))['business']['id']

        new_review = self.app.post(
            '/api/v2/businesses/{}/reviews'.format(business_id),
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()})

        review_id = json.loads(
            new_review.get_data(as_text=True))['review']['id']
        self.app.delete(
            '/api/v2/businesses/{}/reviews/{}'.format(business_id, review_id),
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()})
        exists = db.session.query(
            db.exists().where(Review.title == self.new_review['title']))
        self.assertTrue(exists)

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
            '/api/v2/businesses/',
            data=json.dumps(self.new_business_info),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()
            }
        )

    def register_review(self):
        new_business = self.register_business()
        business_id = json.loads(
            new_business.get_data(as_text=True))['business']['id']

        return self.app.post(
            '/api/v2/businesses/{}/reviews'.format(business_id),
            data=json.dumps(self.new_review),
            headers={
                "content-type": "application/json",
                "x-access-token": self.token()})

    def tearDown(self):
        """Clean-up db"""
        db.session.query(Review).delete()
        db.session.query(Business).delete()
        db.session.query(User).delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
