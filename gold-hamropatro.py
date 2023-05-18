from bs4 import BeautifulSoup
import requests
import json
import re

def fetch_data():
    r = requests.get(
        "https://www.hamropatro.com/gold")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find(
        "ul", {"class": "gold-silver"})
    
    time_table = soup.find(
        "div", {"class": "column12"})
    
    time_string = ""

    # update time
    time = time_table.find_all("b")[0]
    
    
    pattern = r"Last Updated: (.+)"
    match = re.search(pattern, time.text.strip())

    if match:
        extracted_datetime = match.group(1)
        time_string = extracted_datetime.replace(" - ", " ").strip()

    elements = market_table.find_all("li")[1]
    
    markets = []
    
    
    markets.append({
            "time": time_string,
            "price": elements.text.strip().replace("Nrs.", "").strip()
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
