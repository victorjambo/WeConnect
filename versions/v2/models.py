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
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    hash_key = db.Column(db.String(), unique=True, nullable=False)
    activate = db.Column(db.String(), nullable=False)
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

    def __init__(self, username, email, password):
        """Sets defaults for creating user instance
        sets username and email to lower case
        encrypts password
        generates a random hash key
        sets activate to false, this will be changed later
        """
        self.username = username.lower().strip()
        self.email = email.lower().strip()
        self.password = sha256_crypt.encrypt(str(password))
        self.hash_key = uuid.uuid1().hex
        self.activate = False

    def save(self):
        """Commits user instance to the database"""
        db.session.add(self)
        db.session.commit()
        return True


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
    reviews = db.relationship(
        'Review',
        backref='business',
        cascade='all, delete-orphan'
    )

    def save(self):
        """Save a business to the database"""
        db.session.add(self)
        db.session.commit()
        return True


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
    business_id = db.Column(
        db.Integer,
        db.ForeignKey('businesses.id'),
        nullable=False
    )

    def save(self):
        """Save a review to the database"""
        db.session.add(self)
        db.session.commit()
        return True
