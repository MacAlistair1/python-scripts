from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://www.bankbyaj.com/deposite")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find(
        "div", {"class": "bbtable"})
    elements = market_table.find_all("tr")[1:]

    # date = market_table.find_all("p")[0].find('strong').text.replace("Updated as on: ", "").strip()

    # iterate market elements
    markets = []

    for item in elements:
        # extract the information

        markets.append({
            "code": item.find_all("th")[0].find("h3").text.strip(),
            "bank": item.find_all("th")[0].find("span").text.strip(),
            "saving":item.find_all("td")[0].text.strip(),
            "fixed": item.find_all("td")[1].text.strip(),
            # 'lastUpdate': date
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
with open("output/bank_rate.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
