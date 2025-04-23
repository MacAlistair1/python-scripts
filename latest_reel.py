from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import base64
import requests
import time


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--headless")  # Run in headless mode

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL of the Instagram Reel
url = "https://www.instagram.com/nepalivlog.mp4/reels/"

browser.get(url)

time.sleep(10)

# Wait until the <a> element with href containing '/nepalivlog.mp4/reel/' is found
reel_element = WebDriverWait(browser, 40).until(
    EC.presence_of_element_located((By.XPATH, "(//a[contains(@href, '/nepalivlog.mp4/reel/')])[1]"))
)

# Extract the href link from the <a> element
reel_href_full = reel_element.get_attribute("href")
reel_id = reel_href_full.split('/')[5]
reel_href = f"https://www.instagram.com/reel/{reel_id}"

# Grab the content inside the nested <div> and extract the background-image URL
div_element = reel_element.find_element(By.XPATH, ".//div")
background_image_url = div_element.value_of_css_property("background-image")

# Clean up the background image URL to remove the `url()` wrapper
background_image_url = background_image_url.replace('url("', '').replace('")', '')

# Download the image from the background_image_url
response = requests.get(background_image_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert the image to Base64
    image_base64 = base64.b64encode(response.content).decode('utf-8')
else:
    image_base64 = "Failed to download the image."

data = {
    "url": reel_href,
    "image": f"data:image/jpeg;base64,{image_base64}"
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
