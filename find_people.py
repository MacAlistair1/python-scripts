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
# chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
# chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://google.com/search?q="

name = input("Provide Full Exact Name To Find Detail: ") 

if name:
    url = url+name

else:
    url = url+'Nepali Vlog'

try:
    # Open the URL
    browser.get(url)

    # # Parse the page source with BeautifulSoup
    # soup = BeautifulSoup(browser.page_source, "html.parser")
    
    # box = soup.find('a')
    
    # print(box)
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    # browser.quit()
    print('yes final')