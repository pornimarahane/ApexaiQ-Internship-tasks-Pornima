import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TroemnerProduct:
    
    def __init__(self, vendor, product_name, model, description, url, cost):
        self.vendor = vendor
        self.productName = product_name
        self.model = model
        self.description = description
        self.productURL = url
        self.cost = cost

    def as_dict(self):
        return {
            "vendor": self.vendor,
            "productName": self.productName,
            "model": self.model,
            "description": self.description,
            "productURL": self.productURL,
            "cost": self.cost
        }

class TroemnerScraper:
  
    def __init__(self, driver_path, url):
        self.url = url
        self.driver_path = driver_path
        self.data = []

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)

    def _extract_with_regex(self, pattern, text, group=0):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(group).strip() if match else None

    def scrape(self):
        self.driver.get(self.url)

       
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        
        products = self.driver.find_elements(By.XPATH, '//ul[@id="resultsList"]/li')
        print(f"[+] Found {len(products)} products")

        for product in products:
            text_block = product.text.strip()

           
            product_name = self._extract_with_regex(
                r"Weight\s+Set\s+OIML\s*\(?\d*\)?\s*\d+[a-zA-Z]*-\d+[a-zA-Z]*\s+[A-Z]+\d+\s+[A-Za-z]+\s+[A-Za-z]+",
                text_block,
                group=0
            )

            

            model = self._extract_with_regex(r"\(?(\d{6,12})\)?", text_block, group=1)

            
            cost = self._extract_with_regex(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?", text_block)

          
            try:
                url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                url = None

        
            description = re.sub(r"^.*?(?=\n)", "", text_block, flags=re.DOTALL).strip()
            description = re.sub(r"Calibration Certificate.*", "", description, flags=re.DOTALL)
            description = re.sub(r"OIML Class.*", "", description, flags=re.DOTALL)
            description = re.sub(r"Your Price.*", "", description, flags=re.DOTALL)
            description = re.sub(r"\s{2,}", " ", description).strip()

            product_obj = TroemnerProduct(
                vendor="troemner",
                product_name=product_name,
                model=model,
                description=description,
                url=url,
                cost=cost
            )

            self.data.append(product_obj.as_dict())

    def save_to_csv(self, filename="troemner_products.csv",header=False):
        df = pd.DataFrame(self.data)

        import re
        df['description'] = df['description'].apply(
            lambda x: re.sub(r"Item\s*No[:\.]?\s*\d+", "", str(x)).strip()
        )

        df.to_csv(filename="./troemner_products.csv", index=False)
        print(f"[+] Saved {len(df)} products to {filename}")

    def close(self):
        self.driver.quit()


# ------------------- USAGE -------------------
if __name__ == "__main__":
    scraper = TroemnerScraper(
        driver_path=r"C:\Users\porni\OneDrive\Documents\Desktop\Apexa iQ Internship\codes\chromedriver-win64\chromedriver.exe",
        url="https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944"
    )
    scraper.scrape()
    scraper.save_to_csv()
    scraper.close()
