import os

from flask import Flask, render_template, redirect, request, flash, session
import json
from jinja2 import StrictUndefined

from script import query_api
from model import Business, User, UserBusinessLink, AttrAssoc, connect_to_db, db

app = Flask(__name__)

app.secret_key = "jdsfjhggghnrjnjynvcefcrv4c3rv"

app.jinja_env.undefined = StrictUndefined

CLIENT_ID = os.environ['CLIENT_ID']


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():
    """Will show the list of businesses resulting from a search."""
    
    term = str(request.args.get('term'))
    location = str(request.args.get('location'))

    if term == '':
        flash("What are you searching for?")
        return redirect('/')
    else:
        all_results = query_api(term, location)
        businesses = all_results[0]
        num_res = len(businesses)
        rejected = all_results[1]
        num_rejected = len(rejected)

        if businesses == []:
            flash("Sorry, no results matched your search. Try again.")
            return redirect('/')
        else:
            return render_template('results.html', businesses=businesses, num_res=num_res,
                                    term=term, location=location, CLIENT_ID=CLIENT_ID, rejected=rejected,
                                    num_rejected=num_rejected)


@app.route('/details/', methods=['POST', 'GET'])
def display_business_info():
    """Show the specific info for one business.

    request.json is a dictionary with the data of the 

    business clicked on."""

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
                           longitude=longitude, CLIENT_ID=CLIENT_ID)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    username = request.form["username"]
    city = request.form["city"] 
    state = request.form["state"]

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
    """Process login."""

    username = request.form['username']
    password = request.form['password']

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


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]

    flash("Logged Out.")

    return redirect("/")


@app.route('/saving', methods=['POST'])
def save_businessinfo():
    """When the user is logged in, they save the business info to
    
    db when click button."""

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
        new_business = Business(yelp_id=yelp_id, name=name, address=address, city=city, state=state,
                                zipcode=zipcode, phone=phone, neighborhoods=neighborhoods,
                                cross_streets=cross_streets, yelp_url=yelp_url, latitude=latitude,
                                longitude=longitude)
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
    # getting the business object by querying by yelp_id, then get the business_id
        b_obj = Business.query.filter_by(yelp_id=yelp_id).first()
        business_id = b_obj.business_id
        # given the business_id and user_id, query to find user/business assoc obj
        q = UserBusinessLink.query.filter_by(user_id=user_id, business_id=business_id).first()
        if not q:
            business_id = b_obj.business_id
            new_association = UserBusinessLink(user_id=user_id, business_id=business_id)

            db.session.add(new_association)
            db.session.commit()

    return "The ajax post request worked"


@app.route('/userprofile')
def display_user_profile():
    """Display the user's info and the info of businesses they saved."""
    # pulls the username for user that is logged in
    user_id = session['user_id']

    # querying the db base with user_id
    user = User.query.get(user_id)

    # user.businesses is a list of objects.
    businesses = user.businesses

    """Saving attributes to the databse when user clicks on an attribute icon."""

    list_user_business_objs = UserBusinessLink.query.filter_by(user_id=user_id).all()

    # dictionary to store business name with attribute name
    attr_dict = {}
    # user_business_id, user_id, business_id
    for user_business_obj in list_user_business_objs:
        user_business_id = user_business_obj.user_business_id  # get id
        print "user business id: %s" % (user_business_id)
        business_id = user_business_obj.business_id
        # use business_id to query to get name
        business = Business.query.get(business_id)
        business_name = business.name
        print "business name: %s" % (business_name)
        # query by each id
        list_attr_assocs = AttrAssoc.query.filter_by(user_business_id=user_business_id).all()
        print list_attr_assocs
        # check to see if id exists in attr table
        if list_attr_assocs:
            for attr_assoc in list_attr_assocs:
                attr_name = attr_assoc.name
                if business_name not in attr_dict:
                    attr_dict[business_name] = {attr_name: 1}
                else:

                    attr_dict[business_name].update({attr_name: 1})
        else:
            attr_dict[business_name] = {}

    return render_template("profile.html", user=user, businesses=businesses, attr_dict=attr_dict)


@app.route('/saveattr', methods=["POST"])
def save_attr_assoc():
    """When a user clicks on an attr icon next for a saved business, add association to database."""

    attr_name = request.form.get("attrName")
    business_id = request.form.get("businessId")

    user_id = session['user_id']

    # given user_id and business_id, query where the user/business association matches in db
    q = UserBusinessLink.query.filter(UserBusinessLink.user_id == user_id,
                                      UserBusinessLink.business_id == business_id).first()

    # get the user_business_id
    user_business_id = q.user_business_id
    # add new_attr_assoc to  AttrAssoc table!
    new_attr_assoc = AttrAssoc(user_business_id=user_business_id, name=attr_name)

    db.session.add(new_attr_assoc)
    db.session.commit()

    return "Saving attr association"


@app.route('/deleteattr', methods=['POST'])
def delete_attr_assoc():
    """When a user unclicks an attr icon, it is removed from database."""

    attr_name = request.form.get("attrName")
    business_id = request.form.get("businessId")

    user_id = session['user_id']
    # given business_id/user_id, query UserBusiness to get the object
    user_business_obj = UserBusinessLink.query.filter(UserBusinessLink.user_id == user_id,
                                                      UserBusinessLink.business_id == business_id).first()
    # get the user_business_id
    user_business_id = user_business_obj.user_business_id
    # given user_business_id, query AttrAssoc to get object
    obj_to_remove = AttrAssoc.query.filter(AttrAssoc.name == attr_name,
                                           AttrAssoc.user_business_id == user_business_id).first()
    db.session.delete(obj_to_remove)
    db.session.commit()

    return "Removing attr association"


@app.route('/resources')
def resource_articles():
    """When you click on a button or link, go to page of articles."""

    return render_template('resources.html')


if __name__ == "__main__":

    app.debug = False
    
    connect_to_db(app)

    app.run()
