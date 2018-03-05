"""Importing app from __init__
this way we can safely use decorator route()
"""
import jwt
import datetime
from v1 import app, users
from flask_jsonpify import jsonify
from passlib.hash import sha256_crypt
from flask import request, session, make_response
from utils import check_if_name_taken


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
    pass


@app.route('/api/auth/reset-password', methods=['PUT'])
def reset_password():
    """Update user password
    User should be logged in first to update
    """
    pass


@app.route('/api/auth/logout', methods=['DELETE'])
def logout():
    """Destroy user session"""
    pass


@app.route('/api/users', methods=['GET'])
def read_all_users():
    """Reads all users
    """
    pass


@app.route('/api/user/<user_id>', methods=['GET'])
def read_user(user_id):
    """Reads user given an ID
    if user is not provided then user current user ID
    """
    pass


@app.route('/api/user/<user_id>/businesses', methods=['GET'])
def read_user_businesses(user_id):
    """Read all businesses owned by this user"""
    pass
