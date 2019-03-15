import json
import time
import airbnb

api = airbnb.Api()

with open("hrw_settlements.json", "r") as infile:
    items = json.load(infile)

items = [i for i in items if i["airbnb_id"]]

out = []

for item in items:
    airbnb_id = item["airbnb_id"]
    try:
        listing = api.get_listing_details(airbnb_id)
        out.append(listing)
        print('success', airbnb_id)
        time.sleep(1)
    except Exception as e:
        print('failed', airbnb_id)

with open('settlements.json', 'w') as outfile:
    json.dump(out, outfile, indent=2)
