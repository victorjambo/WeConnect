"""Importing app from __init__
this way we can safely use decorator app.route()
"""
from v1 import app


@app.route('/api/businesses', methods=['GET'])
def read_all_businesses():
    """Reads all Businesses"""
    pass


@app.route('/api/businesses', methods=['POST'])
def create_business():
    """Creates a business
    Takes current_user ID and update data
    test if actually saved
    """
    pass


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
