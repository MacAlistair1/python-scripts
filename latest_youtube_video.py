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

# Path to the ChromeDriver executable
chrome_driver_path = "./chromedriver"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--headless")  # Run in headless mode

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL of the YouTube channel
url = "https://www.youtube.com/@nepalivlog/videos"

browser.get(url)

info = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.XPATH, "(//a[@class='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media'])[1]"))
)

videoId = ""

if info:
    videoId = info.get_attribute('href').split('=', 1)[1].strip()

# # Output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# # Write data to text file with proper encoding
with open(os.path.join(output_dir, "latest_yt_video.txt"), "w", encoding="utf-8") as f:
    f.write(videoId)

print("Data successfully written to latest_yt_video.txt")

# Close the browser
browser.quit()