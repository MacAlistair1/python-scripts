from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time
import math
import re

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = "/home4/clickeat/bin/chromium/chrome"
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--headless")  # Run in headless mode

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL of the YouTube channel
url = "https://www.youtube.com/@nepalivlog"

def convert_sci_notation(base, exp):
        return int(base * (10 ** exp))

# Open the URL
browser.get(url)

# Wait for the page to fully load
# time.sleep(5)  # Adjust the sleep time as needed

channel_name = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap"))).text

button = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, '//yt-description-preview-view-model')))
button.click()

description = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.about-section.style-scope.ytd-about-channel-renderer'))).text


info = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@class='description-item style-scope ytd-about-channel-renderer']")))

url = ""
subscriber_count = ""
views = ""
videos = ""


for index, value in enumerate(info):
    if index == 2:
        url = value.text
    elif index == 5:
        subscriber_count = value.text
    elif index == 6:
        videos = value.text
    elif index == 7:
        views = value.text
subscriber_count = subscriber_count.replace(" हजार सदस्यहरू", "").replace("K subscribers", "")
views = views.replace(" भ्यु", "").replace(",", "").replace(" views", "")
videos = videos.replace(",", "").replace(" भिडियोहरू", "").replace(" videos", "")

# Organize data into a dictionary
channel_data = {
    'name': channel_name,
    'url' : url,
    'subscribers': convert_sci_notation(float(subscriber_count), 3),
    'description': description,
    'views' : views,
    'videos' : videos,
}

# # Output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# # Write data to JSON file with proper encoding
with open(os.path.join(output_dir, "channel_info.json"), "w", encoding='utf-8') as f:
    json.dump(channel_data, f, indent=2, ensure_ascii=False)

print("Data successfully written to channel_info.json")

# Close the browser
# browser.quit()