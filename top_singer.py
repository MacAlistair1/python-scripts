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
    
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    singer_list = soup.find_all(
        "h2", {"class": "wp-block-heading"})

    singers = []

    for (index, item) in enumerate(singer_list):
        # extract the information
        
        singers.append({
            "name": item.text.strip(),
        })
        
        if index ==9:
            break

    return singers


# fetch html
html = fetch_data()

# extract data from html
singers = extact_info(html)

# save result in json format
with open("output/top_singer.json", "w") as f:
    f.write(json.dumps(singers, indent=2))
