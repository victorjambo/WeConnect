"""Importing app from __init__
this way we can safely use decorator route()
"""
import os
import jwt
import uuid
import datetime
from flask_jsonpify import jsonify
from passlib.hash import sha256_crypt
from versions import login_required, user_instance
from versions.utils import send_forgot_password_email
from versions.utils import find_user_by_id, check_keys
from flask import request, session, make_response, Blueprint
from versions.utils import validate, check_if_email_taken, password_regex
from versions.utils import check_if_name_taken, find_user_by_name, send_email


mod = Blueprint('user', __name__)


@mod.route('/register', methods=['POST'])
def signup():
    """Creates a user
    first checks if username already exists
    """
    data = request.get_json()

    if validate(data):
        return validate(data)

    if check_if_name_taken(data['username']):
        return jsonify({'warning': 'Username has already been taken'}), 409

    if check_if_email_taken(data['email']):
        return jsonify({'warning': 'Email has already been taken'}), 409

    user_instance.create_user(data)

    if user_instance.users[-1] == data:
        send_email(
            [user_instance.users[-1]['email']],
            user_instance.users[-1]['hash_key'],
            user_instance.users[-1]['username']
        )
        return jsonify({
            'success': 'User created, Check mail box to activate account',
            'user': user_instance.users[-1]['username']
        }), 201

    return jsonify({'warning': 'Could not register user'}), 401


@mod.route('/login', methods=['POST'])
def login():
    """creates new user session and token
    confirms if username and password match
    """
    auth = request.get_json()

    if check_keys(auth, 2):
        return jsonify({'warning': 'Provide username & password'}), 400

    user = find_user_by_name(auth['username'].lower())

    if not user:
        return jsonify({'warning': 'Incorrect username'}), 401

    password = user['password'] if user else None
    candidate_password = auth['password']

    if not password or not auth['username'] or not auth['password']:
        # Incorrect password
        return make_response(
            jsonify({'warning': 'Incorrect password'}),
            401,
            {
                "WWW-Authenticate": "Basic realm='Login Required'"
            }
        )

    if sha256_crypt.verify(candidate_password, password):
        # Sha256 decodes and compares passwords
        # then creates a token that expires in 30 min
        session['logged_in'] = True
        session['username'] = auth['username']
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=999)
        token = jwt.encode(
            {
                'id': user['id'],
                'exp': exp_time
            }, os.getenv("SECRET")
        )
        return jsonify({
            'token': token.decode('UTF-8'),
            'success': 'Login success'
        }), 200

    return make_response(
        jsonify({'warning': 'Cannot Login wrong password'}),
        401,
        {
            "WWW-Authenticate": "Basic realm='Login Required'"
        }
    )


@mod.route('/reset-password', methods=['PUT'])
@login_required
def reset_password(current_user):
    """Update user password
    User should be logged in first to update
    """
    if not current_user:
        return jsonify({'warning': 'Login Again'}), 401

    data = request.get_json()

    if check_keys(data, 2) or not data['password']:
        return jsonify({'warning': 'Provide strong password'}), 400

    if not password_regex.match(data['password']):
        return jsonify({
            'warning': 'Please provide strong password'
        })

    response = find_user_by_id(current_user)
    if sha256_crypt.verify(data['old_password'], response['password']):
        response['password'] = sha256_crypt.encrypt(str(data['password']))
        return jsonify({'success': 'password updated'}), 200

    return jsonify({'warning': 'old password does not match'}), 403


@mod.route('/logout', methods=['DELETE'])
@login_required
def logout(current_user):
    """Destroy user session"""
    if session and session['logged_in']:
        session.clear()
        return jsonify({'success': 'logged out'}), 200
    return jsonify({'warning': 'Already logged out'}), 404


@mod.route("/verify")
def verify():
    """Verify email activation"""
    hash_key = request.args.get('key', default=1, type=str)
    username = request.args.get('name', default=1, type=str)
    response = find_user_by_name(username)
    if response['hash_key'] == hash_key:
        response['activate'] = True
        return jsonify(
            {
                'success': 'Account Activated',
                'key': response
            }
        ), 200

    return jsonify({'warning': 'invalid key error'})


@mod.route("/forgot-password", methods=['POST'])
def forgot_password():
    """Sends new password to your mail"""
    data = request.get_json()
    if data['email'] and check_if_email_taken(data['email']):
        new_password = uuid.uuid4().hex.upper()[0:6]
        for user in user_instance.users:
            if user['email'] == data['email']:
                user['password'] = sha256_crypt.encrypt(new_password)
        send_forgot_password_email([data['email']], new_password)
        return jsonify({'warning': 'Email has been with reset password'}), 200
    return jsonify({'warning': 'No user exists with that email'}), 409
