"""Importing app from __init__
this way we can safely use decorator route()
"""
import os
import jwt
import datetime
from flask_jsonpify import jsonify
from passlib.hash import sha256_crypt
from flask import request, session, make_response, Blueprint
from versions.utils import check_if_name_taken, find_user_by_name
from versions.utils import find_user_by_id, find_business_by_user, check_keys
from versions import login_required, user_instance

mod = Blueprint('user', __name__)


@mod.route('/auth/register', methods=['POST'])
def signup():
    """Creates a user
    first checks if username already exists
    """
    data = request.get_json()
    if check_keys(data, 2):
        return jsonify({'warning': 'Provide username & password'}), 400

    if not data or not data['password'] or not data['username']:
        return jsonify({'warning': 'Cannot create user without password'}), 400

    if not user_instance.password_regex.match(data['username']):
        return jsonify({
            'warning': 'Provide username with more than 4 characters'
        })

    if not user_instance.username_regex.match(data['password']):
        return jsonify({'warning': 'Please provide strong password'})

    if check_if_name_taken(data['username']):
        return jsonify({'warning': 'Username has already been taken'}), 409

    user_instance.create_user(data)

    if user_instance.users[-1] == data:
        return jsonify({
            'success': 'Successfully created user',
            'user': user_instance.users[-1]['username']
        }), 201

    return jsonify({'warning': 'Could not register user'}), 401


@mod.route('/auth/login', methods=['POST'])
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
        """At this point user does not exist
        or either username or password are not provided
        """
        return make_response(
            "Incorrect password",
            401,
            {
                "WWW-Authenticate": "Basic realm='Login Required'"
            }
        )

    if sha256_crypt.verify(candidate_password, password):
        """Sha256 decodes and compares passwords
        then creates a token that expires in 30 min
        """
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
        "Cannot Login",
        401,
        {
            "WWW-Authenticate": "Basic realm='Login Required'"
        }
    )


@mod.route('/auth/reset-password', methods=['PUT'])
@login_required
def reset_password(current_user):
    """Update user password
    User should be logged in first to update
    """
    if not current_user:
        return jsonify({'warning': 'Login Again'}), 401

    data = request.get_json()

    if check_keys(data, 1):
        return jsonify({'warning': 'Provide strong password'}), 400

    if data['password']:
        response = find_user_by_id(current_user)
        response['password'] = sha256_crypt.encrypt(str(data['password']))
        return jsonify({'success': 'password updated'}), 200

    return jsonify({'warning': 'Cannot reset password'}), 403


@mod.route('/auth/logout', methods=['DELETE'])
@login_required
def logout(current_user):
    """Destroy user session"""
    if session and session['logged_in']:
        session.clear()
        return jsonify({'success': 'logged out'}), 200
    return jsonify({'warning': 'Already logged out'}), 404


@mod.route('/users', methods=['GET'])
def read_all_users():
    """Reads all users
    """
    return jsonify({'users': user_instance.users}), 200


@mod.route('/user/<user_id>', methods=['GET'])
@login_required
def read_user(current_user, user_id):
    """Reads user given an ID
    if user is not provided then user current user ID
    """
    response = find_user_by_id(user_id)
    if response:
        return jsonify({'user': response}), 200
    return jsonify({'warning': 'user does not exist'}), 404


@mod.route('/user/<user_id>/businesses', methods=['GET'])
def read_user_businesses(user_id):
    """Read all businesses owned by this user"""
    response = find_business_by_user(user_id)
    if response:
        return jsonify({'user': response}), 200
    return jsonify({'warning': 'user does not own a business'}), 404
