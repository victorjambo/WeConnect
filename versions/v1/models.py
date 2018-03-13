from passlib.hash import sha256_crypt
import re
import uuid


class User(object):
    """user"""
    def __init__(self):
        self.users = []
        self.username_regex = re.compile("[A-z0-9]{4,}")
        self.password_regex = re.compile("[A-z0-9]{4,}")

    def create_user(self, args):
        args['password'] = sha256_crypt.encrypt(str(args['password']))
        args['username'] = args['username'].lower().strip()
        args['id'] = str(len(self.users) + 1)
        args['hash_key'] = uuid.uuid1().hex
        args['activate'] = False
        self.users.append(args)

    def reset_password(self, new_password, response):
        response['password'] = sha256_crypt.encrypt(str(new_password))


class Business(object):
    """Business"""
    def __init__(self):
        self.businesses = []

    def create_business(self, current_user, args):
        args['user_id'] = current_user
        args['id'] = str(len(self.businesses) + 1)
        self.businesses.append(args)


class Review(object):
    """Review"""
    def __init__(self):
        self.reviews = []

    def create_review(self, current_user, businessId, args):
        args['user_id'] = current_user
        args['id'] = str(len(self.reviews) + 1)
        args['business_id'] = businessId
        self.reviews.append(args)
