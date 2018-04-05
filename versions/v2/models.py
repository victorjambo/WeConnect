import uuid
from versions import db
from passlib.hash import sha256_crypt


class User(db.Model):
    """Create table users
    One-to-Many relationship with review and business
    User has many businessess
    User has many reviews
    delete-orphan to delete any attached child
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    fullname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    hash_key = db.Column(db.String(), unique=True, nullable=False)
    activate = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    businesses = db.relationship(
        'Business',
        backref='owner',
        cascade='all, delete-orphan'
    )
    reviews = db.relationship(
        'Review',
        backref='reviewer',
        cascade='all, delete-orphan'
    )
    notifications = db.relationship(
        'Notification',
        backref='recipient',
        cascade='all, delete-orphan'
    )

    def __init__(self, username, fullname, email, password):
        """Sets defaults for creating user instance
        sets username and email to lower case
        encrypts password
        generates a random hash key
        sets activate to false, this will be changed later
        """
        self.username = username.lower().strip()
        self.fullname = fullname
        self.email = email.lower().strip()
        self.password = sha256_crypt.encrypt(str(password))
        self.hash_key = uuid.uuid1().hex
        self.activate = False

    def save(self):
        """Commits user instance to the database"""
        db.session.add(self)
        db.session.commit()


class Business(db.Model):
    """Create table businesses
    One-to-Many relationship with review and user
    business belongs to user
    business has many reviews
    """
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), index=True)
    logo = db.Column(db.String())
    location = db.Column(db.String(), index=True)
    category = db.Column(db.String(), index=True)
    bio = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    reviews = db.relationship(
        'Review',
        backref='business',
        cascade='all, delete-orphan'
    )

    def __init__(self, name=None, logo=None, location=None,
                 category=None, bio=None, owner=None):
        self.name = name
        self.logo = logo
        self.location = location
        self.category = category
        self.bio = bio
        self.owner = owner

    def Search(self, params):
        """Search and filter"""
        page = params['page']
        limit = params['limit']
        location = params['location']
        category = params['category']
        _query = params['_query']

        if _query or location or category:
            if location and _query and not category:
                return self.query.filter(
                    Business.location == location,
                    Business.name.ilike('%' + _query + '%')
                ).paginate(page, limit, error_out=False).items

            if category and _query and not location:
                return self.query.filter(
                    Business.category == category,
                    Business.name.ilike('%' + _query + '%')
                ).paginate(page, limit, error_out=False).items

            if category and location and not _query:
                return self.query.filter(
                    Business.location == location,
                    Business.category == category
                ).paginate(page, limit, error_out=False).items

            if location and not _query and not category:
                return self.query.filter(
                    Business.location == location
                ).paginate(page, limit, error_out=False).items

            if category and not _query and not location:
                return self.query.filter(
                    Business.category == category
                ).paginate(page, limit, error_out=False).items

            return self.query.filter(
                Business.name.ilike('%' + _query + '%')
            ).paginate(page, limit, error_out=False).items

        return self.query.order_by(
            Business.created_at.desc()
        ).paginate(page, limit, error_out=False).items

    def save(self):
        """Save a business to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a given business"""
        db.session.delete(self)
        db.session.commit()


class Review(db.Model):
    """Create table reviews
    One-to-Many relationship with user and business
    review belongs to business
    review belongs to user
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    desc = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey('businesses.id'),
        nullable=False
    )

    def __init__(self, title, desc, business, reviewer):
        self.title = title
        self.desc = desc
        self.business = business
        self.reviewer = reviewer

    def save(self):
        """Save a review to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a given review."""
        db.session.delete(self)
        db.session.commit()


class Notification(db.Model):
    """Handles notifications when user reviews on a business"""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    actor = db.Column(db.String(), nullable=False)
    business_id = db.Column(db.Integer, nullable=False)
    review_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(), nullable=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, recipient, actor, business_id, review_id, read_at=None):
        self.recipient = recipient
        self.actor = actor
        self.business_id = business_id
        self.review_id = review_id
        self.read_at = read_at
        self.action = ' has reviewed your business'

    def save(self):
        """Save a review to the database"""
        db.session.add(self)
        db.session.commit()
