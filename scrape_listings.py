import json
import airbnb

api = airbnb.Api()

with open("settlements.json", "r") as infile:
    items = json.load(infile)

items = [i for i in items if i["airbnb_id"]]

for item in items:
    airbnb_id = item["airbnb_id"]
    listing = api.get_listing_details(airbnb_id)
