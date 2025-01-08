from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL of the Instagram Reel
url = "https://www.instagram.com/_nepalivlog/reels/"

browser.get(url)

# Wait until the <a> element with href containing '/_nepalivlog/reel/' is found
reel_element = WebDriverWait(browser, 40).until(
    EC.presence_of_element_located((By.XPATH, "(//a[contains(@href, '/_nepalivlog/reel/')])[1]"))
)

# Extract the href link from the <a> element
reel_href = reel_element.get_attribute("href")

# Grab the content inside the nested <div> and extract the background-image URL
div_element = reel_element.find_element(By.XPATH, ".//div")
background_image_url = div_element.value_of_css_property("background-image")

# Clean up the background image URL to remove the `url()` wrapper
background_image_url = background_image_url.replace('url("', '').replace('")', '')

data = {
    "url": reel_href,
    "image": background_image_url
}

# Output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# # Write data to JSON file with proper encoding
with open(os.path.join(output_dir, "reel.json"), "w", encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Data successfully written to reel.json")

# Close the browser
browser.quit()
