from versions import user_instance
from flask import jsonify, Blueprint
from versions.utils import find


mod = Blueprint('get_user', __name__)


@mod.route('', methods=['GET'])
def read_all_users():
    """Reads all users
    """
    return jsonify({'users': user_instance.users}), 200


@mod.route('/<user_id>', methods=['GET'])
def read_user(user_id):
    """Reads user given an ID
    if user is not provided then user current user ID
    """
    return find('find_user_by_id', user_id)


@mod.route('/<user_id>/businesses', methods=['GET'])
def read_user_businesses(user_id):
    """Read all businesses owned by this user"""
    return find('find_business_by_user', user_id)
