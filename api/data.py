def business():
    """returns all businesses
    """
    businesses = [
        {
            "id": "1",
            "name": "Samasource",
            "category": "BPO",
            "location": "NBO",
            "bio": "client is always right",
            "user_id": "1"
        },
        {
            "id": "2",
            "name": "Andela",
            "category": "Tech",
            "location": "NBO",
            "bio": "code til you drop",
            "user_id": "1"
        },
        {
            "id": "3",
            "name": "Britam",
            "category": "finance",
            "location": "NBO",
            "bio": "give us your money",
            "user_id": "1"
        },
        {
            "id": "4",
            "name": "Equity",
            "category": "bank",
            "location": "NBO",
            "bio": "wakulima pap",
            "user_id": "2"
        },
        {
            "id": "5",
            "name": "JKUAT",
            "category": "education",
            "location": "NBO",
            "bio": "pay fee, teach yourself",
            "user_id": "2"
        }
    ]
    return businesses


def review():
    """All reviews"""
    reviews = [
        {
            "id": "1",
            "title": "M-Pesa down",
            "desc": "How about you write here",
            "business_id": "1",
            "user_id": "1"
        },
        {
            "id": "2",
            "title": "Good work",
            "desc": "biz 1 user 1 id 2",
            "business_id": "1",
            "user_id": "1"
        },
        {
            "id": "3",
            "title": "Need refund",
            "desc": "id 2 user 2 biz 1",
            "business_id": "1",
            "user_id": "2"
        },
        {
            "id": "4",
            "title": "how come",
            "desc": "id 4 user 2 biz 2",
            "business_id": "2",
            "user_id": "2"
        }
    ]
    return reviews
