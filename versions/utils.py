import re
from flask_mail import Message
from flask import jsonify, render_template
from versions import user_instance, business_instance, review_instance, mail


# User functions
def find_user_by_name(name):
    """Finds user in users array"""
    for user in user_instance.users:
        if user['username'] == name:
            return user
    return None


def find_user_by_id(user_id):
    """find current user record"""
    for user in user_instance.users:
        if user['id'] == user_id:
            return user


def find_business_by_user(user_id):
    all_business = []
    for business in business_instance.businesses:
        if business['user_id'] == user_id:
            all_business.append(business)
    return all_business


def check_if_name_taken(name):
    """Check if username is taken
    """
    if find_user_by_name(name):
        return True
    return False


def check_if_email_taken(email):
    """Check if mail is taken
    """
    for user in user_instance.users:
        if user['email'] == email:
            return True
    return False


# business functions
def find_business_by_id(businessId):
    """find business record"""
    for business in business_instance.businesses:
        if business['id'] == businessId:
            return business


def check_if_biz_name_taken(name):
    for business in business_instance.businesses:
        if business['name'] == name:
            return True
    return False


# reviews functions
def find_reviews_by_business_id(businessId):
    """find review record"""
    all_reviews = []
    for review in review_instance.reviews:
        if review['business_id'] == businessId:
            all_reviews.append(review)
    return all_reviews


def find_review_by_id(reviewId):
    """find review record"""
    for review in review_instance.reviews:
        if review['id'] == reviewId:
            return review


def check_keys(args, length):
    """Check if dict keys are provided
    """
    params = ['email', 'username', 'password', 'old_password', 'fullname']
    for key in args.keys():
        if key not in params or len(args) != length:
            return True
    return False


# validations
username_regex = re.compile("^[a-z0-9_-]{3,15}$")
biz_name_regex = re.compile("[A-z0-9]{4,}")
password_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$")
email_regex = re.compile("[^@]+@[^@]+\.[^@]+")


def validate(data):
    """Validate email password and username
    """
    if check_keys(data, 3):
        return jsonify({
            'warning': 'Provide email, username & password'
        }), 400

    if not data['email'] or not data['password'] or not data['username']:
        return jsonify({
            'warning': 'Cannot create user without all information'
        }), 400

    if not username_regex.match(data['username']):
        return jsonify({
            'warning': 'Provide username with more than 4 characters'
        })

    if not email_regex.match(data['email']):
        return jsonify({
            'warning': 'Please provide valid email'
        })

    if not password_regex.match(data['password']):
        return jsonify({
            'warning': 'Please provide strong password'
        })


# Send Mail
def send_email(recipients, hash_key, username, path):
    """Send email activation
    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support
    """
    msg = Message(
        'Verify Account',
        sender='victormutaijambo@gmail.com',
        recipients=recipients
    )
    msg.html = render_template(
        'email.html', hash_key=hash_key, name=username, path=path)
    mail.send(msg)


def send_forgot_password_email(recipients, new_password):
    """Send email with new password
    """
    msg = Message(
        'Forgot Password',
        sender='victormutaijambo@gmail.com',
        recipients=recipients
    )
    msg.html = render_template(
        'forgotemail.html',
        new_password=new_password
    )
    mail.send(msg)
