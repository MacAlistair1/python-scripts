from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://merolagani.com/LatestMarket.aspx")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find(
        "div", {"id": "ctl00_ContentPlaceHolder1_LiveTrading"})
    elements = market_table.find_all("tr")[1:]

    # iterate market elements
    markets = []

    for item in elements:
        # extract the information
        markets.append({
            "name": item.find_all("td")[0].find("a")['title'],
            "ltp": item.find_all("td")[1].text.strip(),
            "change_%": item.find_all("td")[2].text.strip(),
            "open": item.find_all("td")[4].text.strip(),
            "high": item.find_all("td")[3].text.strip(),
            "low": item.find_all("td")[5].text.strip(),
            "qty": item.find_all("td")[6].text.strip()
        })

    return markets


# fetch html
html = fetch_data()

# extract data from html
markets = extact_info(html)


# display result
for item in markets:
    print(item, "\n")

# save result in json format
with open("output/nepali_market.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
