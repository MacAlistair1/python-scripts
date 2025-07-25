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
import time


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--headless")  # Run in headless mode

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://nepalipatro.com.np"

try:
    # Open the URL
    browser.get(url)
    
    try:
        button = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn_popup_sec')))
        button.click()
    except Exception as e:
        print("An error occurred on button click")

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Extract data
    box = soup.find('div', {'class': "contact-box"})
    circleToday = box.find('div', {'class': 'rectangle-circle-today'})
    nepDate = circleToday.find('div').text.strip()
    nepDay = circleToday.find('span').text.strip().replace(" ", "")
    
    nepYearMonth = box.find("h1").text.strip()
    nepOthers = box.find_all("p")
    nepTithi = nepOthers[0].text.strip()
    
    parts = nepYearMonth.split("ने.सं.")
    nepSambat = "ने.सं. " + parts[1].strip()
    
    try:
        eventBox = box.find('div', {'class': "todaysEvents"})
        nepEvent = eventBox.text.strip()
    except Exception as e:
        nepEvent = ""

    sunBox = box.find("div", {"class": "row"})
    
    sunDivs = sunBox.find_all("div", {"class": "col"})
    
    sunDivs = [div.text.strip() for div in sunDivs]
    
    sunrise = sunDivs[0]
    sunset = sunDivs[1]

    # Organize data into a dictionary
    data = {
        'date': nepDate,
        'day': nepDay,
        'yearMonth': nepYearMonth,
        'sambat': nepSambat,
        'tithi': nepTithi,
        'event': nepEvent,
        'sunrise': sunrise,
        'sunset': sunset
    }

    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Write data to JSON file with proper encoding
    with open(os.path.join(output_dir, "patro.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Data successfully written to patro.json")
    
    time.sleep(2)  # Wait for 2 seconds before scraping events
    
    # Extract data
    projectList = soup.find('div', {'class': "project-list"})

    eventTable = projectList.find('table')
    
    elements = eventTable.find_all('tr')
    
    data = []
    
    for item in elements:
        
        try:
            name = item.find_all('td')[1].find('div', {'class': 'event-list-name'}).text
            date = item.find_all('td')[1].find('small').text
            status = item.find_all('td')[2].find('span', {'class': 'event-list-div'}).text
            img = item.find_all('td')[0].find('img').get("src")
            left = item.find_all('td')[2].find('small').text
        except Exception as e:
            name = item.find_all('td')[1].find('div', {'class': 'event-list-name'}).text
            date = item.find_all('td')[1].find('small').text
            status = item.find_all('td')[2].find('span', {'class': 'event-list-div'}).text
            img = "https://nepalipulse.jeevenlamichhane.com.np/assets/NepaliPulse.png"
            left = ""

        data.append({
            "name": name,
            "img": img,
            "date": date,
            "status" : f'{status} {left}'
        })

    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Write data to JSON file with proper encoding
    with open(os.path.join(output_dir, "events.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Data successfully written to events.json")
    
    

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    browser.quit()
