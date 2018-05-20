"""Importing app from __init__
this way we can safely use decorator app.route()
"""
from flask_jsonpify import jsonify
from flask import request, Blueprint
from versions.utils import find_business_by_id
from versions import business_instance, login_required
from versions.utils import check_if_biz_name_taken, biz_name_regex, find

mod = Blueprint('business', __name__)


@mod.route('', methods=['GET'])
def read_all_businesses():
    """Reads all Businesses"""
    if business_instance.businesses:
        return jsonify({'businesses': business_instance.businesses}), 200
    return jsonify({'warning': 'No Businesses'}), 404


@mod.route('', methods=['POST'])
@login_required
def create_business(current_user):
    """Creates a business
    Takes current_user ID and update data
    test if actually saved
    """
    data = request.get_json()

    if not biz_name_regex.match(data['name']):
        return jsonify({'warning': 'Please provide name with more characters'})

    if check_if_biz_name_taken(data['name']):
        return jsonify({
            'warning': 'Business name {} already taken'.format(data['name'])
        }), 409

    business_instance.create_business(current_user, data)

    if business_instance.businesses[-1] == data:
        return jsonify({
            'success': 'successfully created business',
            'business': business_instance.businesses[-1]
        }), 201

    return jsonify({'warning': 'Could not create new business'}), 401


@mod.route('/<businessId>')
def read_business(businessId):
    """GET Business by id
    Returns single business
    """
    return find('find_business_by_id', businessId)


@mod.route('/<businessId>', methods=['PUT'])
@login_required
def update_business(current_user, businessId):
    """Updates a business given a business ID
    confirms if current user is owner of business
    """
    data = request.get_json()
    response = find_business_by_id(businessId)

    if not response:
        return jsonify({'warning': 'Business Not Found'}), 404

    if current_user != response['user_id']:
        return jsonify({'warning': 'Not Allowed'}), 401

    try:
        if data['name'] and not biz_name_regex.match(data['name']):
            return jsonify({
                'warning': 'Please provide name with more characters'
            })
        response['name'] = data['name'] if data['name'] else response['name']
    except KeyError:
        return jsonify({
            'warning': 'provide business name, leave blank for no update'
        }), 401

    try:
        response['category'] = data['category'] if data['category'] else response['category']
    except KeyError:
        return jsonify({
            'warning': 'provide category, leave blank for no update'
        }), 401

    try:
        response['location'] = data['location'] if data['location'] else response['location']
    except KeyError:
        return jsonify({
            'warning': 'provide location, leave blank for no update'
        }), 401

    try:
        response['bio'] = data['bio'] if data['bio'] else response['bio']
    except KeyError:
        return jsonify({
            'warning': 'provide bio, leave blank for no update'
        }), 401

    return jsonify({
        'success': 'successfully updated',
        'business': response
    }), 201


@mod.route('/<businessId>', methods=['DELETE'])
@login_required
def delete_business(current_user, businessId):
    """Deletes a business
    confirms if current user is owner of business
    """
    response = find_business_by_id(businessId)

    if not response:
        return jsonify({'warning': 'Business Not Found'}), 404

    if current_user != response['user_id']:
        return jsonify({'warning': 'Not Allowed, Contact owner'}), 401

    business_instance.businesses.remove(response)

    return jsonify({
        'success': 'Business Deleted',
        'businesses': business_instance.businesses
    }), 200
