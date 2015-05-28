from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from script import query_api
from model import Business, User, UserBusinessLink, connect_to_db, db

app = Flask(__name__)

app.secret_key = "ABC"
#required to use Flask sessions and the debug toolbar

app.jinja_env.undefined = StrictUndefined
#normally, if you use an undefinted variable in jinja2, it fails silently.
#instead, it will raise an error


@app.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')


@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():
    """Will show the list of businesses resulting from a search"""
    term = str(request.args.get('term'))
    location = str(request.args.get('location'))

    businesses = query_api(term, location)
    num_res = len(businesses)

    if businesses == []:
        flash("Sorry, no results matched your search. Try again.")
        return redirect('/')
    else:
        return render_template('results.html', businesses=businesses, num_res=num_res,
                               term=term, location=location)


@app.route('/details/', methods=['POST', 'GET'])
def display_business_info():
    """Show the specific info for one business"""

    #request.json is a dictionary with the data of the business clicked on
    name = request.args.get('name')
    address = request.args.get('address')
    city = request.args.get('city')
    state = request.args.get('state')
    zipcode = request.args.get('zipcode')
    phone = request.args.get('phone')
    neighborhoods = request.args.get('neighborhoods')
    cross_streets = request.args.get('crossStreets')
    categories = request.args.get('categories')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    yelp_url = request.args.get('yelpUrl')
    rating_stars = request.args.get('urlRatingStars')
    yelp_id = request.args.get('yelpId')

    print latitude
    print longitude

    return render_template('details.html', name=name, address=address, city=city,
                           state=state, zipcode=zipcode, phone=phone, neighborhoods=neighborhoods,
                           cross_streets=cross_streets, categories=categories, yelp_url=yelp_url,
                           rating_stars=rating_stars, yelp_id=yelp_id, latitude=latitude,
                           longitude=longitude)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    username = request.form["username"]
    city = request.form["city"]  # reformat city name to all lower case
    state = request.form["state"]  # dropdown! yay

    q = User.query.filter_by(username=username).all()

    if q:
        flash("This username already exists.")
        return redirect('/register')
    else:
        new_user = User(email=email, username=username, password=password,
                        age=age, city=city, state=state)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.user_id

        flash("User %s added. You are now logged in." % username)
        return redirect('/')


@app.route('/login', methods=['GET'])
def login_page():
    """Show form for user signup."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def user_login():
    """Process login"""
    username = request.form['username']
    password = request.form['password']

    # going to query the database to see if they are in db
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect('/')
    # return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/saving', methods=['POST'])
def save_info():
    """when the user is logged in, they save the business info to db"""

    yelp_id = request.form.get('yelpId')
    name = request.form.get('name')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')
    phone = request.form.get('phone')
    neighborhoods = request.form.get('neighborhoods')
    cross_streets = request.form.get('crossStreets')
    yelp_url = request.form.get('yelpUrl')
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))

    # get username for user that is logged in
    user_id = session['user_id']

    # query to see if this business is in database
    q = Business.query.filter_by(yelp_id=yelp_id).first()

    if not q:
    # if NOT in database, add to database AND association table
        new_business = Business(yelp_id=yelp_id, name=name, address=address,
                                city=city, state=state, zipcode=zipcode, phone=phone,
                                neighborhoods=neighborhoods, cross_streets=cross_streets,
                                yelp_url=yelp_url, latitude=latitude, longitude=longitude)
        print new_business
        db.session.add(new_business)
        db.session.commit()
    # pulling out name from the new_business added above, setting to var business_name
        business_id = new_business.business_id
    # addding to association table
        new_association = UserBusinessLink(user_id=user_id, business_id=business_id)

        db.session.add(new_association)
        db.session.commit()
    else:
    # if IN database, add ONLY to association table
    # getting the business by querying by
        b = Business.query.filter_by(yelp_id=yelp_id).first()
        business_id = b.business_id

        q = UserBusinessLink.query.filter_by(user_id=user_id, business_id=business_id).first()
        if not q:
            # if the association doesn exist
            business_id = b.business_id
            new_association = UserBusinessLink(user_id=user_id, business_id=business_id)

            db.session.add(new_association)
            db.session.commit()

    return "the ajax post request worked"


@app.route('/userprofile')
def display_user_profile():
    """Display the user's info and the info of businesses they saved"""
    # pulls the username for user that is logged in
    user_id = session['user_id']
    print user_id  # correct!
    # querying the db base on username
    user = User.query.get(user_id)

    # user.businesses is a list of objects.
    # prints like -> [<Business name=bi-rite-creamer-san-francisco>] bc __repr__
    businesses = user.businesses

    return render_template("profile.html", user=user, businesses=businesses)


@app.route('/resources')
def resource_articles():
    """When you click on a button or link, go to page of articles"""

    return render_template('resources.html')


if __name__ == "__main__":

    app.debug = True
    #Setting debug=True to invoke the DebugToolbarExtension
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
