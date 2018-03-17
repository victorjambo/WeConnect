"""defines user routes
get all users
get all businesses that belongs to a user
get all reviews that belongs to a user
get one user information
"""
from flask import Blueprint, jsonify, request
from versions.v2.models import User


mod = Blueprint('users_v2', __name__)


@mod.route('/users', methods=['POST'])
def all_users():
    """Reads all users"""
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    new_user.save()
    return jsonify({'success': new_user.username}), 200
