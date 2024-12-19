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


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://nepalhimalpeakprofile.org/peak-profile"

try:
    # Open the URL
    browser.get(url)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Extract data
    table = soup.find('table', {'class': 'mountaintable uk-table uk-table-divider uk-table-small'})
    
    top14 = soup.find('ul', {'class': 'uk-slider-items uk-child-width-1-2@s uk-child-width-1-3@m uk-child-width-1-4@l uk-grid'})
    
    data = []
    topPeaks = []
    
    tbody = table.find('tbody')
    trData = tbody.find_all('tr')
    
    topLiData = top14.find_all('li')
    
    for item in trData:
        peak_id = item.find_all('td')[0].text.strip()
        peak = item.find_all('td')[1].text
        elevation = item.find_all('td')[2].text
        peak_range = item.find_all('td')[3].text
        status = item.find_all('td')[4].text
        
        data.append({
            'id': peak_id,
            'peak': peak,
            'elevation': elevation,
            'range': peak_range,
            'status': status,
        })

    for item in topLiData:
        image = item.find('div', {'class', 'uk-card-media-top'}).find('img').get("src")
        peak = item.find('h5').text.strip().replace("\n", "")
        elevation = item.find('div', {'class', 'el-content uk-panel'}).text.strip()
        
        topPeaks.append({
            'img': image,
            'peak': peak,
            'elevation': elevation
        })

    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Write data to JSON file with proper encoding
    with open(os.path.join(output_dir, "peaks.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    with open(os.path.join(output_dir, "topPeaks.json"), "w", encoding='utf-8') as f:
        json.dump(topPeaks, f, indent=2, ensure_ascii=False)

    print("Data successfully written to peaks.json")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    browser.quit()
