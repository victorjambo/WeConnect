from versions import db


class User(db.Model):
    """Create table users
    One-to-Many relationship with review and business
    User has many businessess
    User has many reviews
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    businesses = db.relationship('Business', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='business', lazy=True)


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
    reviews = db.relationship('Review', backref='business', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


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
