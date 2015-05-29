from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Business(db.Model):
    """When a user saves a business, add info to database."""

    __tablename__ = "businesses"

    business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yelp_id = db.Column(db.String(60), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(60), nullable=True)
    state = db.Column(db.String(2), nullable=True)  # state code
    zipcode = db.Column(db.String(5), nullable=True)
    phone = db.Column(db.String(60), nullable=True)  # better consistent format?
    # categories = db.Column(db.String(60), nullable=True)
    neighborhoods = db.Column(db.String(60), nullable=True)
    cross_streets = db.Column(db.String(60), nullable=True)
    yelp_url = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float(30), nullable=True)
    longitude = db.Column(db.Float(30), nullable=True)

    # define relationship to users table- only need to do in one class
    # params for relationship(class name, table name, name to call class Business/table businesses
    users = db.relationship("User", secondary='users_businesses', backref=db.backref("businesses"))
    attributes = db.relationship("UserBusinessAttr", backref=db.backref("businesses"))

    def __repr__(self):
        """provides helpful representation when printed"""

        return "<Business name=%s>" % (self.yelp_id)


class User(db.Model):
    """Saving User information when they register to make an account"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """provides helpful representation when printed"""

        return "<User name=%s>" % (self.username)


class Attribute(db.Model):
    """Images that represent attributes a user can give a business"""

    __tablename__ = "attributes"

    name = db.Column(db.String(20), primary_key=True)


class UserBusinessAttr(db.Model):
    """Association table of users and the businesses they save to their account"""

    __tablename__ = 'users_businesses'

    user_business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    business_id = db.Column(db.Integer,
                            db.ForeignKey('businesses.business_id'))
    name = db.Column(db.String(20),
                     db.ForeignKey('attributes.name'))


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbproject.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
