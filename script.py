import json
from pprint import pprint
import urllib
import urllib2
import oauth2
from exclude import stores
import os

API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
SEARCH_LIMIT = 6
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
TOKEN = os.environ['TOKEN']
TOKEN_SECRET = os.environ['TOKEN_SECRET']


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API_HOST

    Args:
        host(str): The domain host of the API.
        path(str): The path of the API after the domain.
            (business or search path)
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def search(term=None, location=None):
    """Query the Search API by a search term and location.

    Args:
        term(str): The search term passed to the API.
        location(str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id(str): The ID of the business query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_api(term, location):
    """Queries the API by input values from the user.

    Args:
        term(str): The search term to query.
        location(str): The location of the business to the query.
    """

    response = search(term, location)

    def is_chain(name):
        found = False
        for store_name in stores:
            if store_name in name:
                found = True
        return found

    list_ids = [business['id'] for business in response['businesses'] if not is_chain(business['id'])]

    # running the get_business function by each business_id
    businesses = [get_business(business_id) for business_id in list_ids]
    # businesses is a list of dictionaries. One for each result.

    # accouting for missing info
    for business in businesses:
        if 'display_phone' not in business:
            business['display_phone'] = 'N/A'
        elif 'cross_streets' not in business['location']:
            business['location']['cross_streets'] = 'N/A'
        elif 'neighborhoods' not in business['location']:
            business['location']['neighborhoods'] = 'N/A'
        elif 'coordinates' not in business['location']:
            business['location']['coordinates'] = 'N/A'

    # reformating each dictionary with the info I want to display in a huge list comprehension!

    # NOTE: neighborhoods is still displaying in list [] on screen
    businesses = [{'name': business['name'],
                  'address': ' '.join(business['location']['address']),
                  'city': business['location']['city'],
                  'state': business['location']['state_code'],
                  'zipcode': business['location']['postal_code'],
                  'phone': business['display_phone'],
                  'id': business['id'],
                  'yelp_url': business['url'], 'rating': business['rating'],
                  'categories': ', '.join([i[0] for i in business['categories']]),
                  'url_rating_stars': business['rating_img_url'],
                  'neighborhoods': ', '.join(business['location']['neighborhoods']),
                  'cross_streets': business['location']['cross_streets'],
                  'coordinates': (business['location']['coordinate']['latitude'], business['location']['coordinate']['longitude'])} for business in businesses]

    return businesses
