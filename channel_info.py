from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://www.youtube.com/@nepalivlog/about")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    name = soup.find("meta", itemprop="name").get("content")
    description = soup.find("meta", itemprop="description").get("content")
    
    print(name, description)

    return []


# fetch html
html = fetch_data()

# extract data from html
markets = extact_info(html)


# display result
# for item in markets:
#     print(item, "\n")

# save result in json format
# with open("output/currency.json", "w") as f:
#     f.write(json.dumps(markets, indent=2))
