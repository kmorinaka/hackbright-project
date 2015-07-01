import json
from pprint import pprint
import urllib
import urllib2
import oauth2
from exclude import stores
import os

API_HOST = "api.yelp.com"
SEARCH_PATH = "/v2/search/"
BUSINESS_PATH = "/v2/business/"
SEARCH_LIMIT = 15

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
TOKEN = os.environ["TOKEN"]
TOKEN_SECRET = os.environ["TOKEN_SECRET"]


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
        urllib2.HTTPError: An error occurs from the HTTP request."""

    url_params = url_params or {}
    url = "http://{0}{1}?".format(host, urllib.quote(path.encode("utf8")))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            "oauth_nonce": oauth2.generate_nonce(),
            "oauth_timestamp": oauth2.generate_timestamp(),
            "oauth_token": TOKEN,
            "oauth_consumer_key": CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print u"Querying {0} ...".format(url)

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
        dict: The JSON response from the request."""

    url_params = {
        "term": term.replace(" ", "+"),
        "location": location.replace(" ", "+"),
        "limit": SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id(str): The ID of the business query.

    Returns:
        dict: The JSON response from the request."""

    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_api(term, location):
    """Queries the Yelp APIs by input values from the user.

    Arsearchgs:
        term(str): The search term to query.
        location(str): The location of the business to the query."""

    response = search(term, location)

    def is_chain(name):
        """A filter to check if a business name is a chain based on referencing
        the list, stores in exclude.py"""

        found = False
        for store_name in stores:
            if store_name in name:
                found = True
        return found

    # Keeping track of the businesses that are chains and those that aren't
    chain_businesses = []
    list_ids = []
    for business in response["businesses"]:
        if is_chain(business["id"]):
            chain_businesses.append(business)
        else: 
            list_ids.append(business["id"])

    # Using the business ids to query Yelp's Business API
    # List businesses contains a dicionary for each business
    businesses = [get_business(business_id) for business_id in list_ids]
    
    # Another heuristic to separate chain businesses  
    unique_businesses = []
    for one_business in businesses:
        is_unique = True
        for two_business in businesses:
            if one_business["id"] != two_business["id"] and one_business["name"] == two_business["name"]:
                is_unique = False   
        if is_unique:
            unique_businesses.append(one_business)
        else:
            chain_businesses.append(one_business)
    
    # Not all busineses are categorized 
    for business in unique_businesses:
        if "categories" not in business:
            business["categories"] = [["N/A"]]

    # Restructuring the response list in the case of inconsistent/missing data
    unique_businesses = [{"name": str(business["name"]),
                  "address": " ".join(business["location"]["address"]),
                  "city": business["location"]["city"],
                  "state": business["location"]["state_code"],
                  "zipcode": business["location"]["postal_code"],
                  "phone": business.get("display_phone"),
                  "id": business["id"],
                  "yelp_url": business["url"], "rating": business["rating"],
                  "categories": ", ".join([i[0] for i in business["categories"]]),
                  "url_rating_stars": business["rating_img_url"],
                  "neighborhoods": ", ".join(business["location"].get("neighborhoods", [])) or None,
                  "cross_streets": business["location"].get("cross_streets"),
                  # Will error if latitude and longitude do NOT exist in response
                  "latitude": business["location"]["coordinate"]["latitude"],
                  "longitude": business["location"]["coordinate"]["longitude"]} 
                  for business in unique_businesses]

    # Fixing the address so it doesn't display in a list format
    for reject in chain_businesses:
        reject["address"] = ", ".join(reject["location"]["address"])

    all_results = [unique_businesses, chain_businesses]
    
    return all_results
