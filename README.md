[![Coverage Status](https://coveralls.io/repos/github/victorjambo/WeConnect/badge.svg?branch=ft-api-endpoints)](https://coveralls.io/github/victorjambo/WeConnect?branch=ft-api-endpoints)
[![Build Status](https://travis-ci.org/victorjambo/WeConnect.svg?branch=ft-api-endpoints)](https://travis-ci.org/victorjambo/WeConnect)

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
virtualenv venv
```

Navigate to api folder.
```
cd Weconnect/api
```

Install the packages.
```
pip install -r requirements.txt
```

Confirm your installed packages
```bash
$ pip freeze
```

## Usage

To get the app running...

```bash
$ python app.py
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
POST `/api/auth/register` | Creates a user account 
POST `/api/auth/login` | Logs in a user
POST `/api/auth/logout` | Logs out a user
POST `/api/auth/reset-password` | Password reset
POST  `/api/businesses` | Register a business
PUT `/api/businesses/<businessId>` | Updates a business profile
DELETE `/api//businesses/<businessId>` | Remove a business
GET  `/api/businesses` | Retrieves all businesses
GET  `/api/businesses/<businessId>` | Get a business 
POST  `/api/businesses/<businessId>/reviews` | Add a review for a business
GET  `/api/businesses/<businessId>/reviews` | Get all reviews for a business
