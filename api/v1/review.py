"""Importing app from __init__
this way we can safely use decorator app.route()
"""
from v1 import app


@app.route('/api/businesses/<businessId>/reviews', methods=['POST'])
def create_review(businessId):
    """Create Review given a business ID
    Takes current user ID and business ID then attachs it to response data
    """
    pass


@app.route('/api/businesses/<businessId>/reviews', methods=['GET'])
def read_reviews(businessId):
    """Reads all Review given a business ID"""
    pass


@app.route('/api/businesses/<businessId>/reviews/<reviewId>', methods=['PUT'])
def update_review(reviewId):
    """Updates a Review given a review ID and business ID
    confirms if current user is owner of review
    """
    pass


@app.route(
    '/api/businesses/<businessId>/reviews/<reviewId>',
    methods=['DELETE']
)
def delete_reviews(reviewId):
    """Delete a Review given a review ID and business ID
    confirms if current_user is owner of review
    """
    pass


@app.route('/api/businesses/reviews', methods=['GET'])
def read_all_reviews():
    """Reads all Reviews
    used by admin
    """
    pass
