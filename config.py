import os


class Config(object):
    """BaseClass that defines defaults for child classes
    configure defaults for sending mail with gmail
    sets secret key for authentication
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('GMAIL_MAIL')
    MAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class Development(Config):
    """Sets Debug mode in Development to True"""
    DEBUG = True


class Testing(Config):
    """Testing environment"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_TEST')


class Production(Config):
    """Production environment"""
    DEBUG = False
    TESTING = False
    MAIL_SUPPRESS_SEND = False
