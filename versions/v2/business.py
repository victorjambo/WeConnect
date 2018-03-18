"""Defines routes for CRUD functions in business
Calls methods from Business model
GET: Reads all Businesses
    Fetch all business from db
POST: Creates a business
    Takes current_user ID and update data
GET: Read single business info
PUT: Updates single business
DELETE: Delete single business
"""
from flask import Blueprint, jsonify, request
from versions.v2.models import Business, db, User
from versions import login_required
from versions.utils import biz_name_regex


mod = Blueprint('business_v2', __name__)


@mod.route('/', methods=['GET'])
def read_all_businesses():
    """Reads all Businesses"""
    businesses = Business.query.all()
    if businesses:
        return jsonify(
            [
                {
                    'id': business.id,
                    'name': business.name,
                    'logo': business.logo,
                    'location': business.location,
                    'category': business.category,
                    'bio': business.bio,
                    'owner': business.owner.username,
                    'created_at': business.created_at,
                    'updated_at': business.updated_at
                } for business in businesses
            ]
        ), 200
    return jsonify({'warning': 'No Businesses, create one first'}), 404


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

    # Check if there is an existing business with same name
    if db.session.query(
        db.exists().where(Business.name == data['name'])
    ).scalar():
        return jsonify({
            'warning': 'Business name {} already taken'.format(data['name'])
        }), 409

    business_owner = User.query.get(current_user)

    # create new user instances
    new_business = Business(
        name=data['name'],
        logo=data['logo'],
        location=data['location'],
        category=data['category'],
        bio=data['bio'],
        owner=business_owner
    )

    # Commit changes to db
    new_business.save()

    # Send response if business was saved
    if new_business.id:
        return jsonify({
            'success': 'successfully created business',
            'user': new_business.name
        }), 201

    return jsonify({'warning': 'Could not create new business'}), 401


@mod.route('/<businessId>', methods=['GET'])
def read_business(businessId):
    """Reads Business given a business id"""
    business = Business.query.get(businessId)

    if business:
        return jsonify({
            'business': {
                'id': business.id,
                'name': business.name,
                'logo': business.logo,
                'location': business.location,
                'category': business.category,
                'bio': business.bio,
                'owner': business.owner.username,
                'created_at': business.created_at,
                'updated_at': business.updated_at
            }
        }), 200
    return jsonify({'warning': 'Business Not Found'}), 404


@mod.route('/<businessId>', methods=['DELETE'])
@login_required
def delete_business(current_user, businessId):
    """Deletes a business
    confirms if current user is owner of business
    """
    business = Business.query.get(businessId)

    if not business:
        return jsonify({'warning': 'Business Not Found'}), 404

    name = business.name

    if current_user != business.owner.id:
        return jsonify({'warning': 'Not Allowed, you are not owner'}), 401

    business.delete()

    if not db.session.query(
        db.exists().where(Business.name == name)
    ).scalar():
        return jsonify({'success': 'Business Deleted'}), 200

    return jsonify({'warning': 'Business Not Deleted'}), 400
