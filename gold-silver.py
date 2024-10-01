from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import datetime
from time import gmtime, strftime
def fetch_data():
    r = requests.get(
        "https://www.ashesh.com.np/gold/")

    if r.status_code == 200:

        return r.text
    else:
        raise Exception("Error occur while getting information.")
    

def formatAmount(number):
    number = float(number)
    number = round(number,2)
    is_negative = number < 0
    number = abs(number)
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    value = "".join([r] + d)
    if is_negative:
       value = f'- {value}'
    return value

def extact_info(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # find market elements
    market_table = soup.find_all(
        "div", {"class": "rate_buying"})
    
    
    goldPrice = (market_table[0].text.strip().replace("Rs ", "").strip())
    silverPrice = (market_table[2].text.strip().replace("Rs ", "").strip())
    
    time_table = soup.find(
        "div", {"class": "privacy"})
    
    parts = time_table.text.split("updated on")
    
    
    time_string = ""
    
    if len(parts) > 1:
        time_string = parts[2].strip()    
        date_object = datetime.strptime(time_string, "%d %b %Y")
        formatted_date = date_object.strftime("%d %B %Y")
        current_time = strftime("%H:%M", gmtime())
        time_string = f'{formatted_date} {current_time}'
        

    if goldPrice:
        with open("output/gold.json", "w") as f:
            f.write(json.dumps( [{
                "time": time_string,
                "price": formatAmount(goldPrice).replace(".0", "")
                }], indent=2))
            
    if silverPrice:
        with open("output/silver.json", "w") as f:
            f.write(json.dumps({
                "time": time_string,
                "perTolaPrice": silverPrice,
                "spotPrice" : "",
                "perGramPrice" : "",
                "perKgPrice" : ""
                }, indent=2))


# fetch html
html = fetch_data()

# extract data from html
extact_info(html)


