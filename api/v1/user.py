"""Importing app from __init__
this way we can safely use decorator route()
"""
import jwt
import datetime
from v1 import app, users
from flask_jsonpify import jsonify
from passlib.hash import sha256_crypt
from flask import request, session, make_response
from utils import check_if_name_taken, find_user_by_name
from utils import find_user_by_id, find_business_by_user


@app.route('/api/auth/register', methods=['POST'])
def signup():
    """Creates a user
    first checks if username already exists
    """
    data = request.get_json()
    if not data['password'] or not data['username']:
        return jsonify({'warning': 'password must be present'}), 204

    if check_if_name_taken(data['username']):
        return jsonify({'warning': 'username taken'}), 409

    data['password'] = sha256_crypt.encrypt(str(data['password']))
    data['id'] = str(len(users) + 1)
    users.append(data)

    if users[-1] == data:
        return jsonify({'msg': 'successfully created'}), 201

    return jsonify({'warning': 'Could not register user'}), 401


@app.route('/api/auth/login', methods=['POST'])
def login():
    """creates new user session and token
    confirms if username and password match
    """
    auth = request.get_json()
    user = find_user_by_name(auth['username'])
    password = user['password'] if user else None
    candidate_password = auth['password']

    if not password or not auth['username'] or not auth['password']:
        """At this point user does not exist
        or either username or password are not provided
        """
        return make_response(
            "Incorrect username or password",
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
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
        token = jwt.encode(
            {
                'id': user['id'],
                'exp': exp_time
            }, app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')}), 200


@app.route('/api/auth/reset-password', methods=['PUT'])
def reset_password():
    """Update user password
    User should be logged in first to update
    """
    current_user = '1'
    data = request.get_json()
    response = find_user_by_id(current_user)
    if data['password']:
        response['password'] = sha256_crypt.encrypt(str(data['password']))
        return jsonify({'msg': 'password updated'}), 200
    return jsonify({'warning': 'password cannot be empty'}), 403


@app.route('/api/auth/logout', methods=['DELETE'])
def logout():
    """Destroy user session"""
    session.clear()
    return jsonify({'msg': 'logged out'}), 200


