"""defines user authentication routes
Calls methods from User model
POST: register new user
    check all fields are present
    check if all username or email are taken
    hashes the password before save
POST: Login registered user
    Checks if all fields are present. ie, username & password
    checks if that user exists
    compares passwords
    generate token and creates new session
PUT: reset user password
    Checks session if user is logged in
    validate new password
    checks if all fields are present. ie, old pass & new pass
    compares password
DELETE: logout
    clear user session
POST: forgot password
    Check if email provided exists
    reset user password
    send email with new password
GET: verify/Activate email
    After user registrations an email is sent to new user
"""
from flask import Blueprint, jsonify, request
from versions.v2.models import User, db
from versions.utils import check_keys, send_email
from versions.utils import username_regex, email_regex, password_regex
from functools import wraps


mod = Blueprint('auth_v2', __name__)


def validations(f):
    """Runs validation checks for fields provided before save
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()

        # check if all fields are provided
        if check_keys(data, 3):
            return jsonify({
                'warning': 'All fields. Provide email, username & password'
            }), 400

        # check if username is taken
        if db.session.query(
            db.exists().where(User.username == data['username'])
        ).scalar():
            return jsonify({'warning': 'Username has already been taken'}), 409

        # check if email is taken
        if db.session.query(
            db.exists().where(User.email == data['email'])
        ).scalar():
            return jsonify({'warning': 'Email has already been taken'}), 409

        # validate username
        if not username_regex.match(data['username']):
            return jsonify({
                'warning': 'Provide username with more than 4 characters'
            })

        # validate email
        if not email_regex.match(data['email']):
            return jsonify({
                'warning': 'Please provide valid email'
            })

        # validate password
        if not password_regex.match(data['password']):
            return jsonify({
                'warning': 'Please provide strong password'
            })

        return f(*args, **kwargs)
    return wrap


@mod.route('/register', methods=['POST'])
@validations
def signup():
    """Creates a user"""
    data = request.get_json()

    # create new user instances
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    # Commits new user instance to db
    if new_user.save():
        send_email(
            [new_user.email],
            new_user.hash_key,
            new_user.username
        )
        return jsonify({'success': {
            'username': new_user.username,
            'email': new_user.email,
            'password': new_user.password,
            'hash_key': new_user.hash_key,
            'activate': new_user.activate
        }}), 200

    return jsonify({'warning': 'Could not register user'}), 401
