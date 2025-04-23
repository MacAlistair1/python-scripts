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
chrome_options.binary_location = "/home4/clickeat/bin/chromium/chrome"
chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

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
    nepDate = circleToday.find('h2').text.strip()
    nepDay = circleToday.find('span').text.strip().replace(" ", "")

    mediaBox = box.find('div', {'class': "media-body"})
    nepYearMonth = mediaBox.find("h3").text.strip()
    nepOthers = mediaBox.find_all("p")
    nepSambat = nepOthers[0].text.strip().replace(" ", "")
    nepTithi = nepOthers[1].text.strip()

   
    try:
        eventBox = box.find('div', {'class': "todaysEvents"})
        nepEvent = eventBox.text.strip()
    except Exception as e:
        nepEvent = ""

    sunBox = box.find("div", {"class": "col-12 px-0 mt-2"})
    sunSpans = sunBox.find_all("span")
    sunrise = sunSpans[0].text.strip()
    sunset = sunSpans[1].text.strip()

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
    
    # Extract data
    projectList = soup.find('div', {'class': "project-list"})
    
    eventTable = projectList.find('table', {'class': 'table table-hover mb-0'})
    
    elements = eventTable.find_all('tr')
    
    data = []
    
    
    for item in elements:
        
        try:
            name = item.find_all('td', {'class', 'project-title'})[1].find('div', {'class': 'event-list-name'}).text
            date = item.find_all('td', {'class', 'project-title'})[1].find('small').text
            status = item.find('td', {'class', 'project-status'}).find('i', {'class': 'event-list-div'}).text
            img = item.find('td', {'class', 'project-title'}).find('img').get("src")
            left = item.find('td', {'class', 'project-status'}).find('small').text
        except Exception as e:
            name = item.find_all('td', {'class', 'project-title'})[1].find('div', {'class': 'event-list-name'}).text
            date = item.find_all('td', {'class', 'project-title'})[1].find('small').text
            status = item.find('td', {'class', 'project-status'}).find('i', {'class': 'event-list-div'}).text
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
