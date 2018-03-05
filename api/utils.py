from v1 import users, businesses

""" User functions """


def find_user_by_name(name):
    """Finds user in users array"""
    for user in users:
        if user['username'] == name:
            return user
    return None


def find_user_by_id(user_id):
    """find current user record"""
    for user in users:
        if user['id'] == user_id:
            return user


def find_business_by_user(user_id):
    all_business = []
    for business in businesses:
        if business['user_id'] == user_id:
            all_business.append(business)
    return all_business


def check_if_name_taken(name):
    if find_user_by_name(name):
        return True
    return False


""" business functions """


def find_business_by_id(businessId):
    """find current user record"""
    for business in businesses:
        if business['id'] == businessId:
            return business
