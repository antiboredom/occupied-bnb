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
    listing = api.get_listing_details(airbnb_id)
    out.append(listing)
    time.sleep(1)

with open('sett
