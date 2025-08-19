from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import time

class PaloAltoEOLScraper:
    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.url = url
        self.driver = None

    def setup_driver(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape_table(self, table_xpath):
        self.driver.get(self.url)
        time.sleep(3) 

        table = self.driver.find_element(By.XPATH, table_xpath)
        rows = table.find_elements(By.TAG_NAME, "tr")[1:] 

        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 5:
                vendor = "Palo Alto"

                # Product Name
                product_name = cells[0].text.strip()

                # EOL Date 
                raw_date = cells[2].text.strip()
                eol_date = self.clean_date(raw_date)

                # Resource 
                resource = cells[3].text.strip()
                links = cells[3].find_elements(By.TAG_NAME, "a")
                if links:
                    resource = links[0].get_attribute("href")

                # Recommended Replacement 
                recommended_replacement = cells[-1].text.strip()
                if not recommended_replacement:  
                    recommended_replacement = "-"  

                data.append((vendor, product_name, eol_date, resource, recommended_replacement))
        return data

    def clean_date(self, raw_date):
        
        # Remove  suffixes: st, nd, rd, th
        raw_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', raw_date)

        # Regex match after cleaning
        match = re.search(r"(\w+)\s+(\d{1,2}),\s+(\d{4})", raw_date)
        if match:
            month_str, day, year = match.groups()
            months = {
                "January": "01", "February": "02", "March": "03", "April": "04",
                "May": "05", "June": "06", "July": "07", "August": "08",
                "September": "09", "October": "10", "November": "11", "December": "12"
            }
            month = months.get(month_str, "01")
            return f"{year}-{month}-{int(day):02d}"
    

    def save_to_csv(self, data, output_file="PaloAlto(Hardware).csv"):
        df = pd.DataFrame(data, columns=["Vendor", "Product Name", "EOL Date", "Resource", "Recommended Replacement"])

        df["EOL Date"] = df["EOL Date"].astype(str)
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

    def close_driver(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    DRIVER_PATH = r"C:\Users\porni\OneDrive\Documents\Desktop\Apexa iQ Internship\codes\chromedriver-win64\chromedriver.exe"
    URL = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates"
    TABLE_XPATH = "//table[@class='table table-striped table-hover']"

    scraper = PaloAltoEOLScraper(DRIVER_PATH, URL)
    scraper.setup_driver(headless=True)  
    table_data = scraper.scrape_table(TABLE_XPATH)
    scraper.save_to_csv(table_data)
    scraper.close_driver()
