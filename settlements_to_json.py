from requests_html import HTML
import re
import json

with open("hrw_settlements.html") as infile:
    html = HTML(html=infile.read())

trs = html.find("tbody tr")

items = []

for tr in trs[1:]:
    tds = tr.find("td")
    hrw_id = tds[0]
    settlement_name = tds[1]
    link = settlement_name.find("a", first=True)

    if link is not None:
        url = link.attrs.get("href")
        airbnb_id = re.search(r"rooms\/(\d+)", url).groups(1)[0]
        url = "https://www.airbnb.com/rooms/" + airbnb_id
    else:
        url = None
        airbnb_id = None

    description_israel = tds[2]
    neighborhood_israel = tds[3]
    listing_date = tds[4]

    item = {
        "airbnb_id": airbnb_id,
        "hrw_id": hrw_id.text,
        "url": url,
        "settlement": settlement_name.text,
        "description_israel": description_israel.text,
        "neighborhood_israel": neighborhood_israel.text,
        "date": listing_date.text,
    }

    items.append(item)

with open("hrw_settlements.json", "w") as outfile:
    json.dump(items, outfile, indent=2)
