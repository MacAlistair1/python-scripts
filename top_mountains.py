from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://en.wikipedia.org/wiki/List_of_mountains_in_Nepal")
    if r.status_code == 200:
        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find data elements
    data_table = soup.find(
        "table")
    
    elements = data_table.find_all("tr")[1:]
    
    data = []
    
    for item in elements:
        # extract the information
        
        name = item.find_all("td")[0].find("a").text
        link = item.find_all("td")[0].find("a").get("href")
        height = item.find_all("td")[1].text.strip()+'m'
        note = item.find_all("td")[4].text.strip()

        data.append({
            "name": name,
            "link" : f'https://en.wikipedia.org{link}',
            "height": height,
            "note": note
        })

    return data


# fetch html
html = fetch_data()

# extract data from html
mountains = extact_info(html)

# save result in json format
with open("output/mountains.json", "w") as f:
    f.write(json.dumps(mountains, indent=2))
