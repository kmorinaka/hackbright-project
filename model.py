from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Business(db.Model):
    """Saving yelp business_id, adding it to the db as the yelp_id
        use this id to query the Yelp API later, to display user saved info."""

    __tablename__ = "businesses"

    index = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yelp_id = db.Column(db.String(60), nullable=True)

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

    """This will be an association table? maybe? i dont know
    VVVVVVVV
    user has saved many businesses
    business is saved by many users"""

# class Unknown(db.Model):
#     __tablename__ = "users"

#     user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     yelp_id = db.Column(db.String(64), nullable=False, foreign_key=True)
#     email = db.Column(db.String(64), nullable=False)
#     password = db.Column(db.String(64), nullable=False)
#     gender = db.Column(db.String(10), nullable=True)

#     def __repr__(self):
#         """provides helpful representation when printed"""

#         return "<User name=%s>" % (self.user_name)


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
