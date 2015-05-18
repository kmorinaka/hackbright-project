import requests
from pprint import pprint

etsy_key = 'dp3soepmfkkux0b1kuy2ywu0'
etsy_secret = 'f6rvb2z94o'


def search_etsy(keywords, region):
    etsy_parameters = {
        "api_key": etsy_key,
        "keywords": keywords,
        "region": region,
        "limit": 5,
    }

    r = requests.get("https://openapi.etsy.com/v2/listings/active", params=etsy_parameters).json()
    etsy_listings = []
    count = 0
    pprint(r)
    # for listing in r["results"]:
    #     # # if listing["taxonomy_path"] == ["Art & Collectibles", "Collectibles"]:
    #     # if keywords in listing["title"]:
    #     #     etsy_listings.append(listing)
            #count += 1

    # return etsy_listings # Array of Etsy listings (listing = dictionary)
    # return count, etsy_listings
    # etsy_num_results, etsy_listings = search_etsy(term, min_price, max_price)


# @app.route("/listing/<int:listing_id>")
# def listing_details(listing_id):
#     """Show details about a listing."""

#     r = requests.get("https://openapi.etsy.com/v2/listings/" + str(listing_id) + "?api_key=" + etsy_api_key).json()
#     listing = r["results"][0]

#     return render_template("listing_details.html", title=listing["title"], description=listing["description"], price=listing["price"])
