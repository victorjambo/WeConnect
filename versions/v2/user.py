"""defines user routes
get all users
get all businesses that belongs to a user
get all reviews that belongs to a user
get one user information
"""
from flask import Blueprint, jsonify
from versions.v2.models import User


mod = Blueprint('users_v2', __name__)


@mod.route('/', methods=['GET'])
def get_all_users():
    """Read all users"""
    users = User.query.all()
    return jsonify(
        [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'businesses': user.businesses
            } for user in users
        ]
    ), 200
