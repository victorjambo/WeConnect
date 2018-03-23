"""defines user routes
get all users
get all businesses that belongs to a user
get all reviews that belongs to a user
get one user information
"""
from flask import Blueprint, jsonify
from versions.v2.models import User


mod = Blueprint('users_v2', __name__)


@mod.route('', methods=['GET'])
def get_all_users():
    """Read all users"""
    users = User.query.all()
    if users:
        return jsonify(
            [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'businesses': [
                        {
                            'id': b.id,
                            'name': b.name
                        } for b in user.businesses] if user.businesses else None
                } for user in users
            ]
        ), 200
    return jsonify({'warning': 'No Users'}), 404


@mod.route('/<user_id>', methods=['GET'])
def read_user(user_id):
    """Reads user given an ID"""
    user = User.query.get(user_id)
    if user:
        return jsonify({'user': {
            'username': user.username,
            'id': user.id,
            'activate': user.activate,
            'email': user.email
        }}), 200

    return jsonify({'warning': 'user does not exist'}), 404


@mod.route('/<user_id>/businesses', methods=['GET'])
def read_user_businesses(user_id):
    """Read all businesses owned by this user"""
    user = User.query.get(user_id)
    if user:
        return jsonify(
            [
                {
                    'id': business.id,
                    'name': business.name,
                    'logo': business.logo,
                    'location': business.location,
                    'category': business.category,
                    'bio': business.bio,
                    'created_at': business.created_at,
                    'updated_at': business.updated_at
                } for business in user.businesses
            ] if user.businesses else None
        ), 200

    return jsonify({'warning': 'user does not own a business'}), 404
