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
from functools import wraps
from flask import Flask, request, jsonify, render_template
from versions.v1.models import User, Business, Review
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config.{}'.format(os.getenv('ENVIRON')))
CORS(app)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


user_instance = User()
business_instance = Business()
review_instance = Review()


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
            return jsonify({'warning': 'token missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['id']
        except ValueError:
            return jsonify({'warning': 'token invalid'}), 401

        return f(current_user, *args, **kwargs)
    return wrap


@app.route('/')
def home():
    return render_template('api.html')


import versions.v1.user
import versions.v1.get_user
import versions.v1.business
import versions.v1.review
import versions.manage

app.register_blueprint(versions.v1.user.mod, url_prefix='/api/v1/auth')
app.register_blueprint(versions.v1.get_user.mod, url_prefix='/api/v1')
app.register_blueprint(versions.v1.business.mod, url_prefix='/api/v1')
app.register_blueprint(versions.v1.review.mod, url_prefix='/api/v1')