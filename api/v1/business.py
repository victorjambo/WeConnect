"""Importing app from __init__
this way we can safely use decorator app.route()
"""
from flask_jsonpify import jsonify
from flask import request
from v1 import app, business_instance, login_required
from utils import find_business_by_id


@app.route('/api/businesses', methods=['GET'])
def read_all_businesses():
    """Reads all Businesses"""
    if business_instance.businesses:
        return jsonify(business_instance.businesses), 200
    return jsonify({'warning': 'No Businesses'}), 404


@app.route('/api/businesses', methods=['POST'])
@login_required
def create_business(current_user):
    """Creates a business
    Takes current_user ID and update data
    test if actually saved
    """
    data = request.get_json()
    business_instance.create_business(current_user, data)
    if business_instance.businesses[-1] == data:
        return jsonify({"msg": "business created"}), 201
    return jsonify({"msg": "Could not create new business"}), 401


@app.route('/api/businesses/<businessId>', methods=['GET'])
def read_business(businessId):
    """Reads Business given a business id"""
    response = find_business_by_id(businessId)
    if response:
        return jsonify(response), 200
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

    response['name'] = data['name']
    response['category'] = data['category']
    response['location'] = data['location']
    response['bio'] = data['bio']

    return jsonify({'msg': 'successfully updated'}), 202


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
        return jsonify({'warning': 'Not Allowed'}), 401

    business_instance.businesses.remove(response)

    return jsonify({'msg': 'Deleted'}), 200
