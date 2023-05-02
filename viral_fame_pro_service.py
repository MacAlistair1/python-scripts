from bs4 import BeautifulSoup
import requests
import json


def fetch_data():
    r = requests.get(
        "https://app.smmowl.com/services")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")


def extact_info(html):
     # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    service_table = soup.find("table", {"class": "table"})

    # get all tr elements with the data-filter-table-category-id attribute
    elements = service_table.find_all("tr", {"data-filter-table-category-id": True})

    # iterate market elements
    services = []

    for item in elements:
        # extract the information
        columns = item.find_all("td", {"data-label": "Service"})
    
        for col in columns:
            # print(col.text.strip().split("|")[0])
            
            services.append({
            "name": col.text.strip().split("|")[0].strip(),
            })
            
            break

        

    return services


# fetch html
html = fetch_data()

# extract data from html
services = extact_info(html)


# display result
# for item in services:
#     print(item, "\n")

# save result in json format
with open("output/viral_fame_pro_services.json", "w") as f:
    f.write(json.dumps(services, indent=2))
