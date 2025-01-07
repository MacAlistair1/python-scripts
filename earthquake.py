from bs4 import BeautifulSoup
import requests
import json
import re
from requests.exceptions import RequestException
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extractDate(date):
    match = re.search(r'B\.S\.\:\s*(.*?)\s*A\.D\.:', date) 
    if match:
        return match.group(1)
    else:
        return ""
    
def extractTime(time):
    match = re.search(r'Local:\s*(.*?)\s*UTC:', time) 
    if match:
        return match.group(1)
    else:
        return ""

def fetch_data():
    try:
        r = requests.get("https://seismonepal.gov.np", verify=False)
        if r.status_code == 200:
            return r.text
        else:
                raise Exception("Error occurred while getting information.")
    except RequestException as e:
        print(f"An error occurred: {e}")


def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    table = soup.find("table")

    elements = table.find_all("tr")[1:]

    # iterate market elements
    items = []

    for item in elements:
        # extract the information

        date = item.find_all("td")[1].text.strip()
        time = item.find_all("td")[2].text.strip()
        lat = item.find_all("td")[3].text.strip()
        lon = item.find_all("td")[4].text.strip()
        mag = item.find_all("td")[5].text.strip()
        epi = item.find_all("td")[6].text.strip()
        
        items.append({
            "date" : extractDate(date),
            "time" : extractTime(time),
            "lat" : lat,
            "long" : lon,
            "magnitude" : mag,
            "epicenter" : epi
        })


    return items


# fetch htmcl
html = fetch_data()

# extract data from html
items = extact_info(html)


# # save result in json format
with open("output/earthquakes.json", "w") as f:
    f.write(json.dumps(items, indent=2))