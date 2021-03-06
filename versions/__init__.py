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
from flask import Flask, request, jsonify
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
            return jsonify({
                'warning': 'Missing token. Please register or login'
            }), 401

        is_token_valid = versions.v2.models.AuthToken.query.filter_by(token=token).first()

        is_token_valid = is_token_valid.valid if is_token_valid else True

        if not is_token_valid:
            return jsonify({ 'warning': 'Login again'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['id']
        except jwt.ExpiredSignatureError:
            return jsonify({
                'warning': 'Expired token. Please login to get a new token'
            }), 401
        except ValueError:
            return jsonify({
                'warning': 'Invalid token. Please register or login'
            }), 401

        return f(current_user, *args, **kwargs)
    return wrap

import versions.routes
import versions.v2.models
import versions.v2.auth
import versions.v2.user
import versions.v2.business
import versions.v2.review
import versions.v2.notifications

# version 2 routes
app.register_blueprint(versions.v2.auth.mod, url_prefix='/api/v2/auth')
app.register_blueprint(versions.v2.user.mod, url_prefix='/api/v2/users')
app.register_blueprint(
    versions.v2.business.mod, url_prefix='/api/v2/businesses')
app.register_blueprint(
    versions.v2.review.mod, url_prefix='/api/v2/businesses')
app.register_blueprint(versions.v2.notifications.mod, url_prefix='/api/v2/notifications')
