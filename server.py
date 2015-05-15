from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from script import query_api

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

    return render_template('results.html', businesses=businesses)


# @app.route('/')
# def show_business_profile():
#     """Show the specific info for one business"""

#     return "html for business profile page"


if __name__ == "__main__":

    app.debug = True
    #Setting debug=True to invoke the DebugToolbarExtension

    DebugToolbarExtension(app)

    app.run()
