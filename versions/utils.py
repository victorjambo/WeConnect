from versions import user_instance, business_instance, review_instance
""" User functions """


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
    if find_user_by_name(name):
        return True
    return False


""" business functions """


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


""" reviews functions """


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
    params = ['username', 'password']
    for key in args.keys():
        if key not in params or len(args) != length:
            return True
    return False
