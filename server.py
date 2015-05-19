from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from script import query_api
from model import Business, connect_to_db, db

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


@app.route('/searchresults', methods=['GET'])
def search_results():
    """Will show the list of businesses resulting from a search"""
    term = str(request.args.get('term'))
    location = str(request.args.get('location'))

    businesses = query_api(term, location)

    # add_business = Business(name=name, address=address, city=city, state=state,
    #                         zipcode=zipcode, phone=phone, yelp_id=yelp_id, yelp_url=yelp_url,
    #                         url_rating_stars=url_rating_stars)
    # # db.session.add(add_business)
    # # db.session.commit()
    
    return render_template('results.html', businesses=businesses)


@app.route('/profile')
def show_business_profile(business_name):
    """Show the specific info for one business"""

    return render_template('profile.html')


@app.route('/resources')
def resource_articles():
    """When you click on a button or link, go to page of articles"""

    return render_template('resources.html')


if __name__ == "__main__":

    app.debug = True
    #Setting debug=True to invoke the DebugToolbarExtension

    DebugToolbarExtension(app)

    app.run()
