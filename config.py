import os


class Config(object):
    """docstring for Config"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET')
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    MAIL_USERNAME=os.getenv('GMAIL_MAIL')
    MAIL_PASSWORD=os.getenv('GMAIL_PASSWORD')
    MAIL_SUPPRESS_SEND=True


class Development(Config):
    """docstring for Development"""
    DEBUG = True


class Testing(Config):
    """docstring for Testing"""
    DEBUG = True
    TESTING = True


class Production(Config):
    """"""
    DEBUG = False
    TESTING = False
    MAIL_SUPPRESS_SEND=False