from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import datetime


def fetch_data():
    r = requests.get(
        "https://www.ashesh.com.np/gold/")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find(
        "div", {"class": "rate_buying"})
    
    rate = (market_table.text.strip().replace("Rs ", "").strip())
    
    
    
    
    time_table = soup.find(
        "div", {"class": "privacy"})
    
    parts = time_table.text.split("updated on")
    
    
    time_string = ""
    
    if len(parts) > 1:
        time_string = parts[2].strip()    
        date_object = datetime.strptime(time_string, "%d %b %Y")
        time_string = date_object.strftime("%B %d, %Y")
    
    return [{
            "time": time_string,
            "price": rate
        }]


# fetch html
html = fetch_data()

# extract data from html
markets = extact_info(html)

# save result in json format
with open("output/gold.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
