from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get(
        "https://www.livepriceofgold.com/nepal-gold-price-per-tola.html")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find(
        "div", {"class": "dosya-padding"})

    # update time
    time = market_table.find("time")

    # print(time.text.strip())

    elements = market_table.find_all("tr")[1:]

    # iterate market elements
    markets = []

    for item in elements:
        # extract the information

        markets.append({
            "time": time.text.strip(),
            "price": item.find_all("td")[3].text.strip() + 10731.73
        })

    return markets


# fetch html
html = fetch_data()

# extract data from html
markets = extact_info(html)


# display result
# for item in markets:
#     print(item, "\n")

# save result in json format
with open("output/gold.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
