from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

class GDPTableScraper:
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
        time.sleep(2)  # Allow time for page to load

        table = self.driver.find_element(By.XPATH, table_xpath)
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header

        # Extract Country and 2025 GDP using list comprehension
        data = [
            (
                row.find_elements(By.TAG_NAME, "td")[0].text.strip(),
                row.find_elements(By.TAG_NAME, "td")[4].text.strip()
            )
            for row in rows if len(row.find_elements(By.TAG_NAME, "td")) > 4
        ]

        return data

    def save_to_csv(self, data, output_file):
        # Create DataFrame
        df = pd.DataFrame(data, columns=["Country", "2025[4]"])


        df.to_csv(ScrapTask2_output, index=False)
        print(f"Data saved to {ScrapTask2_output}")

    def close_driver(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    DRIVER_PATH = r"C:\Users\porni\OneDrive\Documents\Desktop\Apexa iQ Internship\codes\chromedriver-win64\chromedriver.exe"
    URL = "https://en.wikipedia.org/wiki/List_of_sovereign_states_in_Europe_by_GDP_(nominal)"
    TABLE_XPATH = '//*[@id="mw-content-text"]/div[1]/div[2]/table'

    scraper = GDPTableScraper(DRIVER_PATH, URL)
    scraper.setup_driver(headless=False)
    table_data = scraper.scrape_table(TABLE_XPATH)
    scraper.save_to_csv(table_data, "ScrapTask2_output.csv")
    scraper.close_driver()
