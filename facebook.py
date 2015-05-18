"""facebook appId: 950035411715285
facebook app secret: b707ea2bc7cdf65813e04c2fb82a36b9
http://graph.facebook.com/oauth/access_token?client_id=950035411715285&client_secret=b707ea2bc7cdf65813e04c2fb82a36b9&grant_type=client_credentials

access_token= 950035411715285|2YIw6VJubFYZuW1EZlkAHuk94Mw
950035411715285|b707ea2bc7cdf65813e04c2fb82a36b9

http://graph.facebook.com/152240831479700
#returned dic of info about ralph's from fb page

searchUrl('https://graph.facebook.com/search?q=%%274154414628%%27&type=page-phone&access_token=CAANgDVs9RNUBACqGhNktuFJf2WCEDCxGPEMyZCU0ubZB2UW495eZAoMAheJc5xaOrgC10vAfeoQxEzRR4UWLZB8ZCni0KeSZBmOra4ntx6rFwKtaZCCjfLi9HP1HB2hBLMvh505RLqCA43Q3SiA9ivO5ZA2GEqQIDSskXpgPFH1iNSdcIzVrUoo0El6TJ4XbfANoWuZA6ZAolSKhYBQ81ueuvU')

{u'website': u'LovingCupSF.com', u'talking_about_count': 11, 
u'category_list': [{u'id': u'197871390225897', u'name': u'Cafe'}, {u'id': u'187153754656815', u'name': u'Dessert Restaurant'}], 
u'likes': 751, u'parking': {u'street': 1, u'lot': 0, u'valet': 0}, 
u'id': u'90156647539', 
u'category': u'Restaurant/cafe', 
u'payment_options': {u'amex': 1, u'cash_only': 1, u'discover': 1, u'mastercard': 1, u'visa': 1}, 
u'has_added_app': False, 
u'can_post': False, 
u'location': {u'city': u'San Francisco', 
    u'zip': u'94109', 
    u'country': u'United States', 
    u'longitude': -122.42236587039, 
    u'state': u'CA', 
    u'street': 
    u'2356 Polk St', 
    u'latitude': 37.798571696375}, 
u'attire': u'Casual', 
u'is_community_page': False, 
u'username': u'lovingcupsf', 
u'description': u"Follow us on Twitter: http://www.twitter.com/LovingCupSF\nPin us on Pinterest: http://www.pinterest.com/LovingCupSF
    \nTag us on Instagram: @LovingCupSF\n\nVisit our second location at 535 Octavia Street in Hayes Valley!! \n\nOur Story: \n\nLoving Cup was founded in 2008 with the intention of offering a dessert shoppe where people can find comforting,
    delicious and healthy treats just like grandma used to make.
    \n\nArmed with a tried and true family recipe for creamy, fluffy  rice pudding, Liz Hawrylo and her mom
    Sandy Hawrylo opened shop in San Francisco's Russian Hill neighborhood.\n\nIn addition to heavenly rice pudding, we offer hand churned, custom blended frozen yogurt--made to order every time with premium ingredients, and absolutely no chemicals or preservatives.\n\nWe are proud to carry all organic dairy products.
    We are a local kind of shop and so are our vendors, like Blue Bottle Coffee out of Oakland and Moonbaby Organic Cupcakes here in SF.", 
u'restaurant_specialties': {u'dinner': 0, u'breakfast': 0, u'coffee': 1, u'lunch': 0, u'drinks': 0}, 
u'hours': {u'sun_1_close': u'22:30', u'sat_1_close': u'22:30', u'sun_1_open': u'11:00', u'fri_1_close': u'22:30', u'thu_1_open': u'12:00', u'tue_1_close': u'21:30', u'sat_1_open': u'11:00', u'mon_1_open': u'12:00', u'mon_1_close': u'21:30', u'wed_1_open': u'12:00', u'wed_1_close': u'21:30', u'tue_1_open': u'12:00', u'fri_1_open': u'12:00', u'thu_1_close': u'21:30'}, 
u'phone': u'(415) 440-6900', u'link': u'https://www.facebook.com/lovingcupsf', u'price_range': u'$ (0-10)', u'checkins': 2368, u'about': u'Local. Organic. All Natural. \n\nSlow-Churned Frozen Yogurt. Homemade Rice Pudding. Extra-Thick Smoothies. Blue Bottle Coffee Service.', 
u'name': u'Loving Cup', 
u'restaurant_services': {u'takeout': 1, u'kids': 1, u'walkins': 1, u'waiter': 0, u'catering': 1, u'delivery': 0, u'outdoor': 0, u'groups': 0, u'reserve': 0}, 
u'cover': {u'source': u'https://scontent.xx.fbcdn.net/hphotos-xfp1/v/t1.0-9/10574465_10152231337322540_1526153717105557055_n.jpg?oh=a382d94e2e7be1f6f21fcfe843cb437b&oe=5602E73A', 
u'cover_id': u'10152231337322540', 
u'offset_x': 0, u'offset_y': 15, u'id': u'10152231337322540'}, 
u'public_transit': u'Muni 19, 41, 45, 47, 49', u'were_here_count': 2368, u'is_published': True}
"""

import requests
import json




SEARCH_URL = 'https://graph.facebook.com/search?q=%%27%(query)s%%27&type=user&access_token=%(token)s'
GRAPH_URL = 'https://graph.facebook.com/'

# Because these are short-lived tokens, we can't manage them with the built in API key management
access_token = 'CAANgDVs9RNUBACqGhNktuFJf2WCEDCxGPEMyZCU0ubZB2UW495eZAoMAheJc5xaOrgC10vAfeoQxEzRR4UWLZB8ZCni0KeSZBmOra4ntx6rFwKtaZCCjfLi9HP1HB2hBLMvh505RLqCA43Q3SiA9ivO5ZA2GEqQIDSskXpgPFH1iNSdcIzVrUoo0El6TJ4XbfANoWuZA6ZAolSKhYBQ81ueuvU'
contacts = [[]]


def search(query):
    id = searchFirstResult(query)
    if id is None:
        #self.output('No results found')
        return "No results found"
   # Use the returned Facebook ID to grab more info
    result = getUserDetailsFromId(id)

    # Parse the JSON response
    username = result.get('username')
    first_name = result.get('first_name')
    last_name = result.get('last_name')
    gender = result.get('gender')
    link = result.get('link')

    # Add the result to the table
    contacts.append([id, query, username, first_name, last_name, gender, link])
    print contacts

def phoneSearch(phone):
        # The logic in here may be hard to follow so I've commented it as
        # best as I possibly can.  Hope it makes sense!
    
        # Remove any formatting leaving just the numbers and mask
        phone = phone.translate(None, " ()-.")
 
        if len(phone) is not 10:
            self.error('Phone number should contain exactly 10 digits')
            return False
 
        if not '*' in phone:
            # Search one phone number and leave
            search(phone)
            return True
 
        # This is to ensure there is only one mask
        # and that the mask characters are all consecutive
        masklen = phone.count('*')
        check = (phone.rfind('*') - phone.find('*')) + 1
 
        if masklen is not check:
            self.error('Mask characters should be consecutive')
            return False
 
        # Replace the mask with a format specifier
        # EX: '****' will be '%04d'
        # EX: '***' will be '%03d'
        fmtString = phone.replace('*'*masklen, '%%0%sd' % masklen)
 
        # Brute force our missing digits 10^masklen
        for x in range(10**masklen):
            # Create our number to search for using the format specifier
            # to fill the string and left pad it with 0's to become a full 10 digits 
            searchNumber = fmtString % x
            search(searchNumber)
        return True
    

def searchUrl(url):
    r = requests.get(url)
    return json.loads(r.content)


def getUserDetailsFromId(id):
    url = GRAPH_URL + id
    results = searchUrl(url)
    return results


def searchFirstResult(query):
    nextUrl = SEARCH_URL % {'query': query, 'token': access_token}
    # Perform the search
    results = searchUrl(nextUrl)
    # Grab the data
    data = results.get('data')
    # Check for errors
    error = results.get('error')

    # Do we have an error?
    if error is not None:
        # If so grab the code
        code = error['code']
        # Is it because our access token expired
        if code is 190:
            # Do something useful here like prompt for a new token          
            print 'Error Code: %s' % (error['code'])
            print 'Message   : %s' % (error['message'])

