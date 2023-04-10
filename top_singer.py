from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://www.worldtop2.com/top-10-nepali-singers-2020")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find(
        "div", {"id": "ez-toc-container"})

    
    elements = market_table.find_all("ul")[0].find_all('li')

    # iterate market elements
    markets = []

    for (index, item) in enumerate(elements):
        # extract the information
        
        markets.append({
            "name": item.find("a").text[3:].strip(),
        })
        
        if(index == 9):
            break
        

    return markets


# fetch html
html = fetch_data()

# extract data from html
markets = extact_info(html)


# display result
# for item in markets:
#     print(item, "\n")

# save result in json format
with open("output/top_singer.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
