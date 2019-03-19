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

bad_images = [
    "images/522932432.jpg",
    "images/192125023.jpg",
    "images/459298663.jpg",
    "images/459314113.jpg",
    "images/522932432.jpg",
    "images/509710836.jpg",
    "images/509709582.jpg",
    "images/459314961.jpg",
    "images/459314113.jpg",
    "images/459298663.jpg",
    "images/458281465.jpg",
    "images/340057260.jpg",
    "images/25874831.jpg",
    "images/192135974.jpg",
    "images/192125094.jpg",
    "images/186504358.jpg",
    "images/126411626.jpg",
    "images/126420972.jpg",
    "images/269834098.jpg",
    "images/509709586.jpg",
    "images/454796559.jpg",
    "images/460231783.jpg",
    "images/450489590.jpg",
    "images/318163765.jpg",
    "images/192136036.jpg",
    "images/186504064.jpg",
    "images/522932954.jpg",
    "images/81556401.jpg",
    "images/427601367.jpg",
    "images/522917413.jpg",
    "images/416002090.jpg",
    "images/522917413.jpg",
    "images/522921897.jpg",
    "images/204792558.jpg",
]

bad_image_ids = [int(i.replace('images/', '').replace('.jpg', '')) for i in bad_images]
print(bad_image_ids)


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
        if image["id"] in bad_image_ids:
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
