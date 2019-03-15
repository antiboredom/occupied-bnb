"""
{
    name: "",
    lat: 1.1,
    lng:1.1,
    real_location: "",
    images: [{id, order}],
    description,
    rating
    price
}
"""

import json
import os

with open("prices.json", "r") as infile:
    prices = json.load(infile)

with open("settlements.json", "r") as infile:
    data = json.load(infile)

with open("tsne-points-1d.json", "r") as infile:
    tsne_images = json.load(infile)


all_images = {}

for image in tsne_images:
    iid = int(image["path"].split("/")[-1].replace(".jpg", ""))
    order = image["point"][0]
    all_images[iid] = order


out = []

for listing in data:
    listing = listing["pdp_listing_detail"]

    lid = listing["id"]

    if "sectioned_description" not in listing:
        print(lid)
        continue

    desc = listing["sectioned_description"]
    name = desc.get("name", "")
    space = desc.get("space", "").replace("\n", " ")
    transit = desc.get("transit", "").replace("\n", " ")
    summary = desc.get("summary", "").replace("\n", " ")

    images = []
    for image in listing["photos"]:
        if not os.path.exists("images/{}.jpg".format(image["id"])):
            continue
        if image["id"] not in all_images:
            continue
        images.append((image["id"], all_images[image["id"]]))

    item = {
        "id": lid,
        "lat": listing["lat"],
        "lng": listing["lng"],
        "name": name,
        "space": space,
        "summary": summary,
        "transit": transit,
        "price": prices.get(str(lid), "?"),
        "rating": listing.get("star_rating", 0),
        "images": images,
    }

    out.append(item)


with open("clean_listings.json", "w") as outfile:
    json.dump(out, outfile)
