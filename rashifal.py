from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import os
from datetime import datetime



# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--headless")  # Run in headless mode

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.hamropatro.com/rashifal"

try:
    # Open the URL
    browser.get(url)


    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Extract data
    box = soup.find('div', {'id': "rashifal"})
    
    rashifalItems = box.find_all('a')
    
    data = []
    
    now = datetime.now()
    readable = now.strftime("%A, %B %d, %Y %I:%M %p")
    
    for rashi in rashifalItems:
        
        name = rashi.find('h3').text
        img = rashi.find('img').get("src")
        text = rashi.find('div', {'class', 'desc'}).text
    
        data.append({
            "name": name,
            "img": f"https://www.hamropatro.com/{img}",
            "rashifal": text,
            'last_updated': readable
        })

    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Write data to JSON file with proper encoding
    with open(os.path.join(output_dir, "rashifal.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Data successfully written to rashifal.json")
    

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    browser.quit()
