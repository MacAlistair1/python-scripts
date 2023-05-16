from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get(
        "https://www.livepriceofgold.com/silver-price/nepal.html")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find(
        "div", {"class": "dt"})

    # update time
    time_div = soup.find(
        "div", {"class": "pad3"})
    time = time_div.find("time")

    elements = market_table.find_all("tr")[1:5]

    # iterate market elements
    markets = []

    for (index, item) in enumerate(elements):
        # extract the information
        markets.insert(index, item.find_all("td")[2].text.replace(" ", ""))

    return ({
        "time": time.text.strip(),
        "spotPrice": markets[0],
        "perGramPrice": markets[1],
        "perKgPrice": markets[2],
        "perTolaPrice": markets[3],
    })


# fetch html
html = fetch_data()

# extract data from html
markets = extact_info(html)


# display result
# for item in markets:
#     print(item, "\n")

# save result in json format
with open("output/silver.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
