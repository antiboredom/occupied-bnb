import json
import requests
import os


def download_file(url, outname):
    if os.path.exists(outname):
        return outname

    with requests.get(url, stream=True) as r:
        with open(outname, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return outname


with open("settlements.json") as infile:
    listings = json.load(infile)

for listing in listings:
    photos = listing["pdp_listing_detail"]["photos"]
    for photo in photos:
        url = photo["large"]
        pid = photo["id"]
        url = url.replace("aki_policy=large", "aki_policy=original")
        outname = "images/{}.jpg".format(pid)
        download_file(url, outname)
