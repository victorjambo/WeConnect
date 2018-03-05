"""Importing app from __init__
this way we can safely use decorator app.route()
"""
from flask_jsonpify import jsonify
from flask import request
from v1 import app, businesses


@app.route('/api/businesses', methods=['GET'])
def read_all_businesses():
    """Reads all Businesses"""
    return jsonify(businesses), 200


@app.route('/api/businesses', methods=['POST'])
def create_business():
    """Creates a business
    Takes current_user ID and update data
    test if actually saved
    """
    current_user = '1'
    data = request.get_json()
    data['user_id'] = current_user
    data['id'] = str(len(businesses) + 1)
    businesses.append(data)
    if businesses[-1] == data:
        return jsonify({"msg": "business created"}), 201
    return jsonify({"msg": "Could not create new business"}), 401


@app.route('/api/businesses/<businessId>', methods=['GET'])
def read_business(businessId):
    """Reads Business given a business id"""
    pass


@app.route('/api/businesses/<businessId>', methods=['PUT'])
def update_business(businessId):
    """Updates a business given a business ID
    confirms if current user is owner of business
    """
    pass


@app.route('/api/businesses/<businessId>', methods=['DELETE'])
def delete_business(businessId):
    """Deletes a business
    confirms if current user is owner of business
    """
    pass
