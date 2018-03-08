"""Importing app from __init__
this way we can safely use decorator app.route()
"""
from flask_jsonpify import jsonify
from flask import request
from v1 import app, business_instance, login_required
from utils import find_business_by_id, check_if_biz_name_taken


@app.route('/api/businesses', methods=['GET'])
def read_all_businesses():
    """Reads all Businesses"""
    if business_instance.businesses:
        return jsonify({'businesses': business_instance.businesses}), 200
    return jsonify({'warning': 'No Businesses'}), 404


@app.route('/api/businesses', methods=['POST'])
@login_required
def create_business(current_user):
    """Creates a business
    Takes current_user ID and update data
    test if actually saved
    """
    data = request.get_json()

    if check_if_biz_name_taken(data['name']):
        return jsonify({
            'warning': 'Business name {} already taken'.format(data['name'])
        }), 409

    business_instance.create_business(current_user, data)

    if business_instance.businesses[-1] == data:
        return jsonify({
            'success': 'successfully created business',
            'user': business_instance.businesses[-1]
        }), 201

    return jsonify({'warning': 'Could not create new business'}), 401


@app.route('/api/businesses/<businessId>', methods=['GET'])
def read_business(businessId):
    """Reads Business given a business id"""
    response = find_business_by_id(businessId)
    if response:
        return jsonify({'business': response}), 200
    return jsonify({'warning': 'Business Not Found'}), 404


@app.route('/api/businesses/<businessId>', methods=['PUT'])
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

    response['name'] = data['name'] if data['name'] else response['name']
    response['category'] = data['category'] if data['category'] else response['category']
    response['location'] = data['location'] if data['location'] else response['location']
    response['bio'] = data['bio'] if data['bio'] else response['bio']

    return jsonify({
        'success': 'successfully updated',
        'business': response
    }), 202


@app.route('/api/businesses/<businessId>', methods=['DELETE'])
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
