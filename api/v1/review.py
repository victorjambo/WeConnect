"""Importing app from __init__
this way we can safely use decorator app.route()
from flask.ext.jsonpify import jsonify
"""
from v1 import app, review_instance, login_required
from flask import request
from flask_jsonpify import jsonify
from utils import find_reviews_by_business_id, find_review_by_id


@app.route('/api/businesses/<businessId>/reviews', methods=['POST'])
@login_required
def create_review(current_user, businessId):
    """Create Review given a business ID
    Takes current user ID and business ID then attachs it to response data
    """
    data = request.get_json()
    review_instance.create_review(current_user, businessId, data)
    if review_instance.reviews[-1] == data:
        return jsonify({'success': 'review successfully created'}), 201
    return jsonify({'warning': 'Could not create new reviews'}), 401


@app.route('/api/businesses/<businessId>/reviews', methods=['GET'])
def read_reviews(businessId):
    """Reads all Review given a business ID"""
    business_reviews = find_reviews_by_business_id(businessId)
    return jsonify({'reviews': business_reviews}), 200


@app.route(
    '/api/businesses/<businessId>/reviews/<reviewId>',
    methods=['DELETE']
)
@login_required
def delete_reviews(current_user, businessId, reviewId):
    """Delete a Review given a review ID and business ID
    confirms if current_user is owner of review
    """
    resp = find_review_by_id(reviewId)
    if not resp:
        return jsonify({'warning': 'Review not found'}), 404

    if current_user != resp['user_id']:
        return jsonify({'warning': 'Not Allowed'}), 401

    if resp['business_id'] == businessId:
        review_instance.reviews.remove(resp)
        return jsonify({'success': 'review deleted'}), 200

    return jsonify({'warning': 'Cannot delete review'}), 404


@app.route('/api/businesses/reviews', methods=['GET'])
@login_required
def read_all_reviews(current_user):
    """Reads all Reviews
    used by admin
    """
    return jsonify({'Reviews': review_instance.reviews}), 200
