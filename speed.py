from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time

# Path to the ChromeDriver executable
chrome_driver_path = "./chromedriver"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--headless")  # Run in headless mode

# Initialize the Chrome WebDriver
service = Service(chrome_driver_path)
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL of the YouTube channel
url = "https://fast.com"


# Open the URL
browser.get(url)

# Wait for the page to fully load
time.sleep(30)  # Adjust the sleep time as needed

downloadSpeed = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".speed-results-container.succeeded"))).text
downloadUnit = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".speed-units-container.succeeded"))).text

uploadSpeed = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "upload-value"))).text
uploadUnit = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "upload-units"))).text

# Organize data into a dictionary
speedData = {
    'download': downloadSpeed,
    'downloadUnit' : downloadUnit,
    'upload': uploadSpeed,
    'uploadUnit' : uploadUnit,
}

# Output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# # Write data to JSON file with proper encoding
with open(os.path.join(output_dir, "speed.json"), "w", encoding='utf-8') as f:
    json.dump(speedData, f, indent=2, ensure_ascii=False)

print("Data successfully written to speed.json")


# Close the browser
browser.quit()