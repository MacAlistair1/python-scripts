from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
import time

# Path to the ChromeDriver executable
chrome_driver_path = "./chromedriver"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

# Initialize the Chrome WebDriver
service = Service(chrome_driver_path)
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://nepalipatro.com.np"

try:
    # Open the URL
    browser.get(url)

    # Give the page some time to load
    time.sleep(5)  # Adjust sleep time if necessary

    # Simulate a click outside the modal to close it
    ActionChains(browser).move_by_offset(10, 10).click().perform()

    # Give some time for the modal to close
    time.sleep(2)

    # Locate the contact-box element using Selenium
    contact_box_element = browser.find_element(By.CLASS_NAME, "sticky-top")

    # Take a screenshot of the contact-box element
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    screenshot_path = os.path.join(output_dir, "contact_box_screenshot.png")
    contact_box_element.screenshot(screenshot_path)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    browser.quit()
