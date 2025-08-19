import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime

class PaloAltoProduct:
    def __init__(self, software_name, version, release_date, eol_date):
        self.softwareName = software_name
        self.version = version
        self.releaseDate = release_date
        self.eolDate = eol_date

    def as_dict(self):
        return {
            "softwareName": self.softwareName,
            "version": self.version,
            "releaseDate": self.releaseDate,
            "eolDate": self.eolDate
        }

class PaloAltoScraper:
    def __init__(self, driver_path, url):
        self.url = url
        self.driver_path = driver_path
        self.data = []

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)

        self.xpaths = [
            '//*[@id="prisma-access-browser"]',
            '//*[@id="qradar"]/following-sibling::table[1]',  # QRadar special case
            '//*[@id="pan-os-panorama"]',
            '//*[@id="panorama-plugin"]',
            '//*[@id="traps-esm-and-cortex"]',
            '//*[@id="cortex-xsoar"]',
            '//*[@id="globalprotect"]',
            '//*[@id="prisma-cloud-compute"]',
            '//*[@id="lightcyber-magna"]',
            '//*[@id="evident-io"]',
            '//*[@id="cloudgenix"]',
            '//*[@id="brightcloud-subscription"]',
            '//*[@id="vm-series-models"]'
        ]

    def _normalize_date(self, text):
        if not text or text.strip() in ["-", "null", ""]:
            return "-"
        text = text.strip()
        for fmt in ["%m/%d/%Y", "%m/%d/%y", "%B %d, %Y", "%b %d, %Y", "%B %Y"]:
            try:
                return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
            except:
                continue
        return text  # keep original if not parseable

    def _get_heading(self, table):
        """Find the heading text above the table."""
        for tag in ["h2", "h3", "h4", "b", "strong", "p"]:
            try:
                h = table.find_element(By.XPATH, f"./preceding-sibling::{tag}[1]").text.strip()
                if h:
                    return h
            except:
                continue
        return "Unknown"

    def scrape(self):
        self.driver.get(self.url)
        time.sleep(3)

        for idx, xp in enumerate(self.xpaths, start=1):
            try:
                table = self.driver.find_element(By.XPATH, xp)
            except:
                print(f"[!] Table not found for xpath: {xp}")
                continue

            heading = self._get_heading(table)
            rows = table.find_elements(By.XPATH, ".//tr")
            if not rows:
                continue

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue

                texts = [c.text.strip() for c in cells]

                # Skip header or redundant rows
                if any(word in " ".join(texts).lower() for word in ["version", "release", "end of life", "eol", "support"]):
                    continue

                version, release_date, eol_date = "-", "-", "-"

                # Special handling for QRadar (2nd xpath)
                if idx == 2:
                    # QRadar tables: first column is the actual version
                    if len(texts) >= 2:
                        version = texts[0]
                        release_date = texts[1] if len(texts) > 1 else "-"
                        eol_date = texts[2] if len(texts) > 2 else "-"
                else:
                    # Normal case: [version, release_date, eol_date]
                    if len(texts) == 2:
                        version, eol_date = texts
                    elif len(texts) == 3:
                        version, release_date, eol_date = texts
                    elif len(texts) >= 4:
                        version, release_date, eol_date = texts[0:3]

                release_date = self._normalize_date(release_date)
                eol_date = self._normalize_date(eol_date)

                product = PaloAltoProduct(
                    software_name=heading,
                    version=version,
                    release_date=release_date,
                    eol_date=eol_date
                )
                self.data.append(product.as_dict())

    def save_to_csv(self, filename="paltoaltosoftware.csv"):
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"[+] Saved {len(df)} records to {filename}")

    def close(self):
        self.driver.quit()


# ------------------- USAGE -------------------
if __name__ == "__main__":
    scraper = PaloAltoScraper(
        driver_path=r"C:\Users\porni\OneDrive\Documents\Desktop\Apexa iQ Internship\codes\chromedriver-win64\chromedriver.exe",
        url="https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"
    )
    scraper.scrape()
    scraper.save_to_csv()
    scraper.close()
