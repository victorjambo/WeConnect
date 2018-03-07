"""Modulizing the app
Split the routes into modules i.e User, Business, Review

object `app` is created here so that each module can import it safely
and the __name__ variable will resolve to the correct package.

Its important to import the modules after the application object is created.

Why do this; it reduces lines of code within a single file
and its an easy read
"""
import os
import jwt
from flask import Flask, request, jsonify
from functools import wraps
from data import business, review
from utils import find_user_by_id

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET')


def login_required(f):
    """Ensures user is logged in before action
    Checks of token is provided in header
    decodes the token then returns current user info
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'warning': 'token missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = find_user_by_id(data['id'])
        except ValueError:
            return jsonify({'warning': 'token invalid'}), 401

        return f(current_user, *args, **kwargs)
    return wrap


users = []
businesses = business()
reviews = review()

import v1.user
import v1.business
import v1.review
