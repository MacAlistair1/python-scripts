from bs4 import BeautifulSoup
import requests
import json
import re
from requests.exceptions import RequestException
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_data():
    try:
        r = requests.get("http://noc.org.np/retailprice", verify=False)
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

    elements = table.find_all("tr")[9:]

    # iterate market elements
    items = []

    for item in elements:
        # extract the information

        date = item.find_all("td")[0].text.strip()
        
        start_index = date.index("(") + 1  # Find the index of the opening parenthesis and add 1 to skip it
        end_index = date.index(")")  # Find the index of the closing parenthesis
        text = date[start_index:end_index]  # Get the text inside the parentheses
        # text = date.split('(', 1)[0].strip()
        
        text = text.replace(".", "/")  # Replace dots with slashes in the extracted text

        items.append({
            "date": text,
            "time": item.find_all("td")[1].text.strip(),
            "petrol": item.find_all("td")[2].text.strip(),
            "diesel": item.find_all("td")[4].text.strip(),
            "kerosene": item.find_all("td")[3].text.strip(),
            "lpg": item.find_all("td")[5].text.strip()
        })

        break

    return items


# fetch htmcl
html = fetch_data()

# extract data from html
items = extact_info(html)


# # display result
# for item in items:
#     print(item, "\n")

# # save result in json format
with open("output/oil.json", "w") as f:
    f.write(json.dumps(items, indent=2))
