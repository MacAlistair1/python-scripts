import requests
import json
from datetime import datetime
import time


def fetch_data():
    r = requests.get("https://www.bollytube.online/rest/bollystats/getTopNepaliSongs")

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Error occur while getting information.")


def extact_info(data):

    # iterate market elements
    markets = []

    for item in data:
        
        iso_string = item['lastUpdated']  # e.g., "2025-07-21T23:26:02.413+00:00"

        # Parse the ISO 8601 string to a datetime object
        dt = datetime.fromisoformat(iso_string)
        # Convert to epoch milliseconds
        epoch_millis = int(dt.timestamp() * 1000)
        
        # extract the information    
        markets.append({
            "title": item['title'],
            "videoId": item['videoId'],
            "views":item['views'],
            'lastUpdate': epoch_millis
        })
        

    return markets


# fetch html
html = fetch_data()

# extract data from html
markets = extact_info(html)


# display result
# for item in markets:
#     print(item, "\n")

# save result in json format
with open("output/top_music_video.json", "w") as f:
    f.write(json.dumps(markets, indent=2))
