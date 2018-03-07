"""Modulizing the app
Split the routes into modules i.e User, Business, Review

object `app` is created here so that each module can import it safely
and the __name__ variable will resolve to the correct package.

Its important to import the modules after the application object is created.

Why do this; it reduces lines of code within a single file
and its an easy read
"""
import os
from flask import Flask
from v1.models import User, Business, Review

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET')

user_instance = User()
business_instance = Business()
review_instance = Review()

import v1.user
import v1.business
import v1.review
