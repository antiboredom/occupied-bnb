import json
import time
import requests

base = "https://www.airbnb.com/api/v2/pdp_listing_booking_details?_format=for_web_dateless&_intents=p3_book_it&_interaction_type=pageload&_p3_impression_id=p3_1552520120_con%2FMRJw4xlFD6zi&_parent_request_uuid=a23f08cc-f28a-48d8-85e9-c05735e18ff9&currency=USD&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={}&locale=en&number_of_adults=1&number_of_children=0&number_of_infants=0&show_smart_promotion=0"

with open('settlements.json', 'r') as infile:
    listings = json.load(infile)


out = {}

for l in listings:
    l = l["pdp_listing_detail"]
    lid = l["id"]
    try:
        r = requests.get(base.format(lid)).json()
        price = r["pdp_listing_booking_details"][0]["p3_display_rate"]["amount"]
        out[lid] = price
        with open('prices.json', 'w') as outfile:
            json.dump(out, outfile)
        time.sleep(2)
    except Exception as e:
        print(e)

