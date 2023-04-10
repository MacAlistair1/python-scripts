import requests
import json


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
        # extract the information    
        markets.append({
            "title": item['title'],
            "videoId": item['videoId'],
            "views":item['views'],
            'lastUpdate': item['lastUpdated']
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
