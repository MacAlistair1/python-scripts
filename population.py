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

province = ""
district = ""
url = f"https://censusnepal.cbs.gov.np/results/population?province={province}&district={district}"

try:
    # Open the URL
    browser.get(url)
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Extract data
    popBox = soup.find_all('div', {'class': "highlight-card"})
    totalPopulation = popBox[0].find('h3').text.strip()
    mfSvg = popBox[0].find('svg')
    
    sexRatio = popBox[1].find('h3').text.strip()
    sexRatioTxt = popBox[1].find('span', {'class' : 'text-xs'}).text.strip()
    
    density = popBox[2].find('h3').text.strip()
    densityTxt = popBox[2].find('span', {'class' : 'text-xs'}).text.strip()
    
    annualPopGrowth = popBox[3].find('h3').text.strip()+"%"
    
    populationDisability = popBox[4].find('h3').text.strip()+"%"
    femaleDisability = popBox[5].find('h3').text.strip()+"%"
    maleDisability = popBox[6].find('h3').text.strip()+"%"
    
    data = {
        'totalPopulation': totalPopulation,
        'mFSvg': str(mfSvg),
        'sexRatio': sexRatio,
        'sexRatioTxt': sexRatioTxt,
        'density': density,
        'densityTxt': densityTxt,
        'annualPopGrowth': annualPopGrowth,
        'populationDisability': populationDisability,
        'femaleDisability': femaleDisability,   
        'maleDisability': maleDisability,   
    }
    
    
    # # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Write data to JSON file with proper encoding
    with open(os.path.join(output_dir, "population.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Data successfully written to population.json")
    
    

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    browser.quit()
