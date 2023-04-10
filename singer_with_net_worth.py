from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://popnable.com/stories/51152-the-most-famous-nepali-musicians-in-2022")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find("table")

    
    elements = market_table.find_all("tr")[1:]

    # iterate market elements
    markets = []

    for item in (elements):
        # extract the information
        markets.append({
            "name": item.find_all("td")[0].text.strip(),
            "networth": item.find_all("td")[1].text.strip(),
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
with open("output/top_singer_by_networth.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
