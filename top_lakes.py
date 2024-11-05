from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get("https://www.thirdrockadventures.com/blog/lakes-in-nepal")
    if r.status_code == 200:
        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find data elements
    data_table = soup.find(
        "div", {"class": "notecontent"})
    
    elements = data_table.find_all('ul')
    
    
    data = []
    
    for item in elements:
        # extract the information
        
        for li in item.find_all('li'):
            
            name = li.text.split('.', 1)[-1].strip()
            link = li.find("a").get("href")
            
            data.append({
                "name": name,
                "link": f'https://www.thirdrockadventures.com/blog/lakes-in-nepal{link}',
            })

    return data


# fetch html
html = fetch_data()

# extract data from html
lakes = extact_info(html)

# save result in json format
with open("output/lakes.json", "w") as f:
    f.write(json.dumps(lakes, indent=2))
