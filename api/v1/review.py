"""Importing app from __init__
this way we can safely use decorator app.route()
from flask.ext.jsonpify import jsonify
"""
from v1 import app, reviews
from flask import request
from flask_jsonpify import jsonify
from utils import find_reviews_by_business_id, find_review_by_id


@app.route('/api/businesses/<businessId>/reviews', methods=['POST'])
def create_review(businessId):
    """Create Review given a business ID
    Takes current user ID and business ID then attachs it to response data
    """
    current_user = '1'
    data = request.get_json()
    data['user_id'] = current_user
    data['id'] = str(len(reviews) + 1)
    data['business_id'] = businessId
    reviews.append(data)
    if reviews[-1] == data:
        return jsonify({"msg": "review created"}), 201
    return jsonify({"msg": "Could not create new reviews"}), 401


@app.route('/api/businesses/<businessId>/reviews', methods=['GET'])
def read_reviews(businessId):
    """Reads all Review given a business ID"""
    business_reviews = find_reviews_by_business_id(businessId)
    return jsonify({'reviews': business_reviews}), 200


@app.route(
    '/api/businesses/<businessId>/reviews/<reviewId>',
    methods=['DELETE']
)
def delete_reviews(businessId, reviewId):
    """Delete a Review given a review ID and business ID
    confirms if current_user is owner of review
    """
    resp = find_review_by_id(reviewId)
    if not resp:
        return jsonify({'msg': 'Review not found'}), 404
    if resp['business_id'] == businessId:
        reviews.remove(resp)
        return jsonify({'msg': 'review deleted'}), 200
    return jsonify({'msg': 'Cannot delete review'}), 404


@app.route('/api/businesses/reviews', methods=['GET'])
def read_all_reviews():
    """Reads all Reviews
    used by admin
    """
    return jsonify(reviews), 200
