from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import pandas as pd


class TroemnerScraper:
    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

    def fetch_items(self):
        self.driver.get(self.url)

        # wait until products load
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"product-tile")]'))
        )
        time.sleep(2)

        products = self.driver.find_elements(By.XPATH, '//div[contains(@class,"product-tile")]')
        items = []

        for product in products:
            try:
                # Product Name (Card Title)
                title_elem = product.find_element(By.XPATH, './/a[contains(@class,"product-name")]')
                title = title_elem.text.strip()

                # Hover link (product page link)
                link = title_elem.get_attribute("href")

                # Description
                desc_elem = product.find_element(By.XPATH, './/div[contains(@class,"product-description")]')
                description = desc_elem.text.strip()

                # Price
                try:
                    price_elem = product.find_element(By.XPATH, './/span[contains(@class,"sales")]')
                    price = price_elem.text.strip()
                except:
                    price = "N/A"

                # Model (extract numeric codes using regex)
                model_match = re.search(r'\b\d{5,}\b', description)
                model = model_match.group(0) if model_match else "N/A"

                # Vendor (static for now)
                vendor = "Troemner"

                items.append({
                    "Vendor": vendor,
                    "ProductName": title,
                    "Model": model,
                    "Description": description,
                    "Link": link,
                    "Price": price
                })

            except Exception as e:
                print("Error parsing product:", e)

        return items

    def scrape(self):
        data = self.fetch_items()
        df = pd.DataFrame(data)
        print(df)
        df.to_csv("troemner_products.csv", index=False)
        self.driver.quit()


if __name__ == "__main__":
    DRIVER_PATH = r"C:\Users\porni\OneDrive\Documents\Desktop\Apexa iQ Internship\codes\chromedriver-win64\chromedriver.exe"
    URL = "https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944"
    
    scraper = TroemnerScraper(DRIVER_PATH, URL)
    scraper.scrape()
