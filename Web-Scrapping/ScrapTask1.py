from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import time

class TallestBuildingsScraper:
    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.url = url
        self.driver = None

    def setup_driver(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--start-maximized")
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape_table(self, table_xpath):
        self.driver.get(self.url)
        time.sleep(3)  

        table = self.driver.find_element(By.XPATH, table_xpath)
        rows = table.find_elements(By.TAG_NAME, "tr")[2:]  

        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 5:
                # Regex 
                number_match = re.search(r"^(.*?)\n", cells[0].text)
                name_match = re.search(r"^(.*?)\n", cells[1].text)
                height_match = re.search(r"\n(.*?)\n", cells[3].text)
                floors_match = re.search(r"\n(.*?)\n", cells[4].text)
                city_match = re.search(r"^(.*?)\n", cells[6].text)
                country_match = re.search(r"\n(.*?)\n", cells[-4].text)
                year_match = re.search(r"\n(.*?)\n", cells[-3].text)
                comments_match = re.search(r"^(.*?)\n", cells[-2].text)
                
                
                number = number_match.group(1).strip() if name_match else cells[0].text.strip()
                name = name_match.group(1).strip() if name_match else cells[1].text.strip()
                height = height_match.group(1).strip() if height_match else cells[3].text.strip()
                floors = floors_match.group(1).strip() if height_match else cells[4].text.strip()
                city = city_match.group(1).strip() if city_match else cells[6].text.strip()
                country = country_match.group(1).strip() if height_match else cells[-4].text.strip()
                year = year_match.group(1).strip() if height_match else cells[-3].text.strip()
                comments = comments_match.group(1).strip() if height_match else cells[-2].text.strip()

                
                
                data.append((number, name,  height, floors, city, country,year, comments ))
        
        return data

    def save_to_csv(self, data, output_file=None):
        df = pd.DataFrame(data, columns=["Number", "Name",  "height", "Floors", "City","Country", "Year", "Comments"])
        df.to_csv("ScrapTask1_output.csv", index=False)  
        print(f"Data saved to ScrapTask1_output.csv")

    def close_driver(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    DRIVER_PATH = r"C:\Users\porni\OneDrive\Documents\Desktop\Apexa iQ Internship\codes\chromedriver-win64\chromedriver.exe"
    URL = "https://en.wikipedia.org/wiki/List_of_tallest_buildings"
    TABLE_XPATH = '//*[@id="mw-content-text"]/div[1]/div[7]/table[2]'
    
    scraper = TallestBuildingsScraper(DRIVER_PATH, URL)
    scraper.setup_driver(headless=False)  
    table_data = scraper.scrape_table(TABLE_XPATH)
    scraper.save_to_csv(table_data)
    scraper.close_driver()
