from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Business(db.Model):
    """Business that returned from a query"""

    __tablename__ = "businesses"

    business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yelp_id = db.Column(db.String(60), nullable=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    zipcode = db.Column(db.String(15), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    yelp_url = db.Column(db.String(100), nullable=True)
    yelp_rating = db.Column(db.Float, nullable=True)
    url_rating_stars = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """provides helpful representation when printed"""

        return "<Business name=%s>" % (self.name)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."