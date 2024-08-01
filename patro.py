from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import os

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

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Extract data
    box = soup.find('div', {'class': "contact-box"})
    circleToday = box.find('div', {'class': 'rectangle-circle-today'})
    nepDate = circleToday.find('h2').text.strip()
    nepDay = circleToday.find('span').text.strip().replace(" ", "")

    mediaBox = box.find('div', {'class': "media-body"})
    nepYearMonth = mediaBox.find("h3").text.strip()
    nepOthers = mediaBox.findAll("p")
    nepSambat = nepOthers[0].text.strip().replace(" ", "")
    nepTithi = nepOthers[1].text.strip()

   
    try:
        eventBox = box.find('div', {'class': "todaysEvents"})
        nepEvent = eventBox.text.strip()
    except Exception as e:
        nepEvent = ""

    sunBox = box.find("div", {"class": "col-12 px-0 mt-2"})
    sunSpans = sunBox.findAll("span")
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

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    browser.quit()
