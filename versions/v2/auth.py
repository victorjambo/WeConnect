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
app.url_map
"""
from flask import Blueprint, jsonify, request, session, redirect
from versions.v2.models import User, db, AuthToken
from versions.utils import check_keys, send_email, send_forgot_password_email
from versions.utils import username_regex, email_regex, password_regex
from passlib.hash import sha256_crypt
import datetime
from functools import wraps
import os
from versions import login_required
import jwt
import uuid


mod = Blueprint('auth_v2', __name__)


def validations(f):
    """Runs validation checks for fields provided before save
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()

        # check if all fields are provided
        if check_keys(data, 4):
            return jsonify({
                'warning': 'All Fields Required'
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
        if not username_regex.match(data['username'].lower()):
            return jsonify({
                'warning': 'Invalid username'
            }), 409

        # validate email
        if not email_regex.match(data['email']):
            return jsonify({
                'warning': 'Invalid email'
            }), 409

        # validate password
        if not password_regex.match(data['password']):
            return jsonify({
                'warning': 'Provide strong password'
            }), 409

        return f(*args, **kwargs)
    return wrap


def validate_new_password(f):
    """Check if password is strong enough"""
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        if check_keys(data, 2) or not data['password']:
            return jsonify({'warning': 'Provide strong password'}), 400

        if not password_regex.match(data['password']):
            return jsonify({
                'warning': 'Provide strong password'
            }), 400
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
        fullname=data['fullname'],
        email=data['email'],
        password=data['password']
    )

    # Commits new user instance to db
    new_user.save()
    if new_user.id:
        send_email(
            [new_user.email],
            new_user.hash_key,
            new_user.username,
            'auth_v2'
        )
        return jsonify({'success': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'password': new_user.password,
            'hash_key': new_user.hash_key,
            'activate': new_user.activate
        }}), 200

    return jsonify({'warning': 'Could not register user'}), 401


@mod.route('/login', methods=['POST'])
def login():
    """Login registered user"""
    auth = request.get_json()

    # validate all fields are present
    if check_keys(auth, 2):
        return jsonify({'warning': 'Provide username & password'}), 400

    user = User.query.filter_by(username=auth['username']).first()

    if not user:
        return jsonify({
            'warning': '{} does not exist'.format(auth['username'])
        }), 401

    password = user.password
    candidate_password = auth['password']

    if sha256_crypt.verify(candidate_password, password):
        # Sha256 decodes and compares passwords
        # then creates a token that expires in 30 min
        session['logged_in'] = True
        session['username'] = auth['username']
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode(
            {
                'id': user.id,
                'username': user.username,
                'exp': exp_time
            }, os.getenv("SECRET")
        )
        AuthToken(token.decode('UTF-8')).save()
        return jsonify({
            'token': token.decode('UTF-8'),
            'success': 'Login success'
        }), 200

    return jsonify({'warning': 'Cannot Login wrong password'}), 401


@mod.route('/reset-password', methods=['PUT'])
@validate_new_password
@login_required
def reset_password(current_user):
    """Update user password
    User should be logged in first to update
    """
    if not current_user:
        return jsonify({'warning': 'Login Again'}), 401

    data = request.get_json()

    user = User.query.get(current_user)

    if sha256_crypt.verify(data['old_password'], user.password):
        user.password = sha256_crypt.encrypt(str(data['password']))
        user.save()
        return jsonify({'success': 'password updated'}), 200

    return jsonify({'warning': 'old password does not match'}), 403


@mod.route("/forgot-password", methods=['POST'])
def forgot_password():
    """Sends new password to your mail"""
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    # check if email is taken
    if data['email'] and user:
        new_password = uuid.uuid4().hex.upper()[0:6]
        user.password = sha256_crypt.encrypt(new_password)
        user.save()
        send_forgot_password_email([data['email']], new_password)
        return jsonify({'success': 'Email has been sent with new password'}), 200

    return jsonify({'warning': 'No user exists with that email'}), 409


@mod.route('/logout', methods=['DELETE'])
@login_required
def logout(current_user):
    """Destroy user session"""
    token_from_request = request.headers['x-access-token']
    instance_tokens = AuthToken.query.filter_by(token=token_from_request).first()
    if instance_tokens:
        instance_tokens.valid = False
        instance_tokens.save()
        return jsonify({'success': 'logged out'}), 200
    return jsonify({'message': 'Invalid token!'}), 401


@mod.route("/verify")
def verify():
    """Verify email activation"""
    hash_key = request.args.get('key', default=1, type=str)
    name = request.args.get('name', default=1, type=str)
    user = User.query.filter_by(username=name).first()
    if user.hash_key == hash_key:
        user.activate = True
        user.save()
    return redirect(os.getenv("DESTINATION_URL")), 301
