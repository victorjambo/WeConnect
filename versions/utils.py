import re
from flask_mail import Message
from flask import jsonify, render_template
from versions import mail
from versions.v2.models import Business, db, User

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
        }), 400

    if not email_regex.match(data['email']):
        return jsonify({
            'warning': 'Please provide valid email'
        }), 400

    if not password_regex.match(data['password']):
        return jsonify({
            'warning': 'Please provide strong password'
        }), 400


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

def existing_module(module, name):
    modules = { 'user': User, 'business': Business }
    if db.session.query(
            db.exists().where(modules[module].name == name)
        ).scalar():
        return True
    return False

def get_in_module(module, businessId):
    modules = { 'user': User, 'business': Business }
    return modules[module].query.get(businessId)

def check_email(email):
    if db.session.query(
            db.exists().where(User.email == email)
        ).scalar():
        return True
    return False
