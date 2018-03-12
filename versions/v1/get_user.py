from versions import user_instance
from flask import jsonify, Blueprint
from versions.utils import find_user_by_id, find_business_by_user


mod = Blueprint('get_user', __name__)


@mod.route('/users', methods=['GET'])
def read_all_users():
    """Reads all users
    """
    return jsonify({'users': user_instance.users}), 200


@mod.route('/user/<user_id>', methods=['GET'])
def read_user(user_id):
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
