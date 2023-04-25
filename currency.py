from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://www.nrb.org.np/forex/")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # date
    date_text = soup.find(
        "div", {"class": "body-h3"}).text.replace('Showing Exchange Rate for ', '').strip()

    # find market elements
    market_table = soup.find_all(
        "table", {"class": "table"})

    elements = market_table[1].find_all("tr")[1:]

    india = market_table[0].find_all("tr")[1]

    # iterate market elements
    markets = []

    # fixed indian price
    markets.append({
        "name": india.find_all("td")[0].find("div", {"class": "ml-2"}).find("span", {"class": "text-capitalize"}
                                                                            ).text.replace('(', '').replace(')', ''),
        "code": india.find_all("td")[0].find("div", {"class": "ml-2"}).text[:4].strip(),
        "unit": 1,
        "buy": round(float(india.find_all("td")[2].text.strip())/100, 2),
        "sell": round(float(india.find_all("td")[3].text.strip())/100, 2),
        "date": date_text,
    })

    for item in elements:
        # extract the information

        raw = item.find_all("td")[0].find("div", {"class": "ml-2"})
        name = raw.find("span", {"class": "text-capitalize"}
                        ).text.replace('(', '').replace(')', '')
        code = raw.text[:4].strip().upper()

        unit = int(item.find_all("td")[1].text.strip())

        buy = round(float(item.find_all("td")[2].text.strip()), 2)

        sell = round(float(item.find_all("td")[3].text.strip()),2)

        if (unit == 100):
            buy = buy/100
            sell = sell/100

        markets.append({
            "name": name,
            "code": code,
            "unit": 1,
            "buy": buy,
            "sell": sell,
            "date": date_text,
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
with open("output/currency.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
