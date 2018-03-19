"""Defines routes for CRUD functions in review
Calls methods from Business model
POST: Create Review given a business ID
    uses businessID and current_user to create the relationship
GET: Reads all Review for a businessID
PUT: Updates a review
    expects businessID, current_user and reviewID as arguments
DELETE: Deletes a Review
    expects businessID, current_user and reviewID as arguments
"""
from flask import Blueprint, jsonify, request
from versions.v2.models import Business, db, User, Review
from versions import login_required
from functools import wraps

mod = Blueprint('review_v2', __name__)


def precheck(f):
    """Checks if businessID is available
    Check if business belongs to current user
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        business = Business.query.get(kwargs['businessId'])
        review = Review.query.get(kwargs['reviewId'])

        if not business:
            return jsonify({'warning': 'Business Not Found'}), 404

        if not review:
            return jsonify({'warning': 'Review Not Found'}), 404

        if args[0] != review.reviewer.id:
            return jsonify({'warning': 'Not Allowed, you are not owner'}), 401

        return f(*args, **kwargs)
    return wrap


@mod.route('/<businessId>/reviews', methods=['POST'])
@login_required
def create_review(current_user, businessId):
    """Create Review given a business ID
    Takes current user ID and business ID then attachs it to response data
    """
    data = request.get_json()
    _reviewer = User.query.get(current_user)
    _business = Business.query.get(businessId)

    if not _business:
        return jsonify({'warning': 'Business Not Found'}), 404

    # create new review instances
    new_review = Review(
        title=data['title'],
        desc=data['desc'],
        business=_business,
        reviewer=_reviewer
    )

    # Commit changes to db
    new_review.save()

    # Send response if business was saved
    if new_review.id:
        return jsonify({
            'success': 'successfully created business',
            'review': {
                'id': new_review.id,
                'title': new_review.title,
                'reviewer': new_review.reviewer.username,
                'desc': new_review.desc
            }
        }), 201

    return jsonify({'warning': 'Could not create new reviews'}), 401


@mod.route('/<businessId>/reviews', methods=['GET'])
def read_review(businessId):
    """Reads all Review given a business ID"""
    business = Business.query.get(businessId)
    if not business:
        return jsonify({'warning': 'Business Not Found'}), 404

    if business.reviews:
        return jsonify({'reviews': [
            {
                'id': review.id,
                'title': review.title,
                'desc': review.desc,
                'reviewer': review.reviewer.username,
                'business': review.business.name,
                'created_at': review.created_at,
                'updated_at': review.updated_at,
            } for review in business.reviews
        ]}), 200

    return jsonify({'warning': 'Business has no reviews'}), 404


@mod.route('/<businessId>/reviews/<reviewId>', methods=['DELETE'])
@login_required
@precheck
def delete_review(current_user, businessId, reviewId):
    """Delete a Review given a review ID and business ID
    confirms if current_user is owner of review
    """
    review = Review.query.get(reviewId)
    title = review.title
    review.delete()

    if not db.session.query(
        db.exists().where(Review.title == title)
    ).scalar():
        return jsonify({'success': 'Review Deleted'}), 200

    return jsonify({'warning': 'Review Not Deleted'}), 400


@mod.route('/reviews', methods=['GET'])
@login_required
def read_all_reviews(current_user):
    """Reads all Reviews"""
    reviews = Review.query.all()
    if reviews:
        return jsonify({'Reviews': [
            {
                'id': review.id,
                'title': review.title,
                'desc': review.desc,
                'reviewer': review.reviewer.username,
                'business': review.business.name,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            } for review in reviews
        ]}), 200

    return jsonify({'warning': 'No Review, create one first'}), 404


@mod.route('/<businessId>/reviews/<reviewId>', methods=['PUT'])
@login_required
@precheck
def update_business(current_user, businessId, reviewId):
    """Updates a review given a business ID
    confirms if current user is owner of business
    """
    data = request.get_json()
    review = Review.query.get(reviewId)

    review.title = data['title']
    review.desc = data['desc']

    review.save()

    if review.title == data['title']:
        return jsonify({
            'success': 'successfully updated',
            'review': {
                'id': review.id,
                'title': review.title,
                'desc': review.desc,
                'reviewer': review.reviewer.username,
                'business': review.business.name,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            }
        }), 201

    return jsonify({'warning': 'Review Not Updated'}), 400
