import json
import pprint
import urllib
import urllib2
import oauth2
from exclude import stores


API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
SEARCH_LIMIT = 5

CONSUMER_KEY = "g3dgBew3xq4aHZ14JGF-9Q"
CONSUMER_SECRET = "-jhY-JQLTweu0vVvHj_oXuYYruk"
TOKEN = "52YIkIAyQfNkasjTsSUHwRwQ44Nr4IbU"
TOKEN_SECRET = "bp3Ck0_JhOpFfyPBdtOIa3FdhZg"


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


def search(term, location):
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

    #response is a dic wiht key businesses: [list of dictionaries for each business]
    businesses = response.get('businesses')
    #businesses is a list of top results based on number specified in SEARCH_LIMIT

    print len(businesses)
    #pprint.pprint(businesses, indent=2)

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    avoid = []
    #list of business ids to avoid/exclude
    list_ids = []
    # for i in range(len(businesses)):
    #     for s in stores:
    #         if s in businesses[i]['id']:
    #             avoid.append(businesses[i]['id'])
    #             businesses.pop(businesses.index(businesses[i]))
    #         else:
    #             list_ids.append(businesses[i]['id'])
    for i in range(len(businesses)):
        list_ids.append(businesses[i]['id'])

    for s in stores:
        for business_id in list_ids:
            if s in business_id:
                avoid.append(business_id)
                list_ids.pop(list_ids.index(business_id))

    print "HERE ARE THE LISTS"
    print list_ids
    print avoid

    """YOU LEFT OFF HERE:

    what printed in terminal
    list_ids = [u'ocean-pacific-market-huntington-beach', u'ralphs-huntington-beach-2']
    avoid = [u'trader-joes-huntington-beach', u'ralphs-huntington-beach-4', u'ralphs-irvine-3']
    Why did it take out some ralphs, but not all?? """
    #get business ids for first 5 businesses (5 is SEARCH_LIMIT)

    response_list = []
    for business_id in list_ids:
        response_list.append(get_business(business_id))
    #take the list_ids, run each through the get_business function to make request to business API
    #put each search result into a response list

    print u'Result for business "{0}" found:'.format(business_id)
    #pprint.pprint(response, indent=2)

    #for response in response_list:
        #return response_list[:5]
        #search limit 15 or > to weed out duplicate locations, only return 5 results to screen
    
    #return response_list
    #response_list is list of dictionaries w/ info for each business result
