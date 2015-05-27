from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from script import query_api
from model import Business, User, connect_to_db, db

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
    yelp_url = request.args.get('yelpUrl')
    rating_stars = request.args.get('urlRatingStars')
    yelp_id = request.args.get('yelpId')

    return render_template('details.html', name=name, address=address, city=city,
                           state=state, zipcode=zipcode, phone=phone, neighborhoods=neighborhoods,
                           cross_streets=cross_streets, categories=categories, yelp_url=yelp_url,
                           rating_stars=rating_stars, yelp_id=yelp_id)


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
    state = request.form["state"]  # Make form only accept state code 'CA'

    q = User.query.filter_by(username=username).all()

    if q:
        flash("This user already had an account.")
        return redirect('/login')
    else:
        new_user = User(email=email, username=username, password=password,
                        age=age, city=city, state=state)

        db.session.add(new_user)
        db.session.commit()
        # username = new_user.username
        # # print username
        # session['username'] = username
        # print session

        flash("User %s added." % username)
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
    name = request.form.get('name')

    return "the ajax post request worked"


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
