from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from script import query_api
# from model import Business, connect_to_db, db

app = Flask(__name__)

app.secret_key = "ABC"
#required to use Flask sessions and the debug toolbar

app.jinja_env.undefined = StrictUndefined
#normally, if you use an undefinted variable in jinja2, it fails silently.
#instead, it will raise an error


@app.route('/')
def index():
    """Homepage"""
    # r = "https://sitestream.twitter.com/1.1/site.json?follow=6253282"

    return render_template('homepage.html')


@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():
    """Will show the list of businesses resulting from a search"""
    term = str(request.args.get('term'))
    location = str(request.args.get('location'))

    businesses = query_api(term, location)

    return render_template('results.html', businesses=businesses)


@app.route('/profile', methods=['POST', 'GET'])
def display_business_info():
    """Show the specific info for one business

    LEFT OFF HERE. FIGURE OUT HOW TO PUT THE DATA ON 'profile.html'
    """
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

    return render_template('profile.html', name=name, address=address, city=city,
                           state=state, zipcode=zipcode, phone=phone, neighborhoods=neighborhoods,
                           cross_streets=cross_streets, categories=categories, yelp_url=yelp_url,
                           rating_stars=rating_stars)


# @app.route('/', methods=['GET'])
# def display_info():
  

@app.route('/resources')
def resource_articles():
    """When you click on a button or link, go to page of articles"""

    return render_template('resources.html')


if __name__ == "__main__":

    app.debug = True
    #Setting debug=True to invoke the DebugToolbarExtension

    DebugToolbarExtension(app)

    app.run()
