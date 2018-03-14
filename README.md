[![Build Status](https://travis-ci.org/victorjambo/WeConnect.svg?branch=ft-api-endpoints)](https://travis-ci.org/victorjambo/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/victorjambo/WeConnect/badge.svg?branch=ft-api-endpoints)](https://coveralls.io/github/victorjambo/WeConnect?branch=ft-api-endpoints)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/dfd1f513767a4227aa2202c14a7f4c59)](https://www.codacy.com/app/victorjambo/WeConnect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=victorjambo/WeConnect&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/4020562f1eb41bcf63f9/maintainability)](https://codeclimate.com/github/victorjambo/WeConnect/maintainability)

# WeConnect

WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with. 

## Installation
For the UI designs to work you need a working browser like google chrome

Clone the repository into your local environment

```
git clone git@github.com:victorjambo/WeConnect.git
```

Change directory into WeConnect

```
cd WeConnect/designs/UI
```

Run `index.html` file in your browser

## Api Installation
To set up WeConnect API, make sure that you have python3, postman and pip installed.

Use [virtualenv](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) for an isolated working environment.

Clone the Repo into a folder of your choice
```
git clone https://github.com/victorjambo/WeConnect.git
```

Create a virtual enviroment.
```
virtualenv venv --python=python3
```

Navigate to api folder.
```
cd WeConnect
```

Install the packages.
```
pip3 install -r requirements.txt
```

Confirm your installed packages
```bash
$ pip freeze
```
Set environment variables for `SECRET`, `SUPPRESSED`, `GMAIL_MAIL` and `GMAIL_PASSWORD`
> SECRET is your secret key
> SUPPRESSED is either `True` or `False`. Set True if you don't want email to be sent during testing and development
> `GMAIL_MAIL` and `GMAIL_PASSWORD` got to `https://myaccount.google.com/apppasswords` and generate app password for your api

## Usage

To get the app running...

```bash
$ python3 app.py
```

Open Postman and run endpoints

## Test

To run you test use

```bash
$ nosetests
```

To test endpoints manually fire up postman and run the following endpoints

**EndPoint** | **Functionality**
--- | ---
POST `/api/v1/auth/register` | Creates a user account 
POST `/api/v1/auth/login` | Logs in a user
POST `/api/v1/auth/logout` | Logs out a user
POST `/api/v1/auth/reset-password` | Password reset
POST  `/api/v1/businesses` | Register a business
PUT `/api/v1/business/<businessId>` | Updates a business profile
DELETE `/api/v1/business/<businessId>` | Remove a business
GET  `/api/v1/businesses` | Retrieves all businesses
GET  `/api/v1/business/<businessId>` | Get a business 
POST  `/api/v1/business/<businessId>/reviews` | Add a review for a business
GET  `/api/v1/business/<businessId>/reviews` | Get all reviews for a business


# API Documentation
View API documentation from
```
https://weconnect7.docs.apiary.io
```