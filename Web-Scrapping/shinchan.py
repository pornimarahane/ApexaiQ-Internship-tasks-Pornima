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

        # Special xpaths where first row contains real software name
        self.special_software_name_xpaths = {2, 9, 11}

        self.xpaths = [
            '//*[@id="prisma-access-browser"]',
            '//*[@id="qradar"]/following-sibling::table[1]',
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

    def _normalize_row(self, texts):
        """Normalize row into (version, release_date, eol_date)."""
        while len(texts) < 3:
            texts.append("-")
        return texts[0].strip(), self._normalize_date(texts[1]), self._normalize_date(texts[2])

    def _get_software_name(self, xp, idx):
        """Get section software name from heading or fallback."""
        try:
            for tag in ["h2", "h3", "h4", "b", "strong", "p"]:
                elem = self.driver.find_element(By.XPATH, xp + f"/preceding-sibling::{tag}[1]")
                name = elem.text.strip()
                if name:
                    return name
        except:
            pass
        if idx in self.special_software_name_xpaths:
            return None
        return xp.split('"')[1]

    def scrape(self):
        self.driver.get(self.url)
        time.sleep(3)

        for idx, xp in enumerate(self.xpaths, start=1):
            try:
                table = self.driver.find_element(By.XPATH, xp)
            except:
                print(f"[!] Table not found for xpath: {xp}")
                continue

            rows = table.find_elements(By.XPATH, ".//tr")
            if not rows:
                continue

            software_name = self._get_software_name(xp, idx)
            special_first_value = None

            for i, row in enumerate(rows):
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue

                texts = [c.text.strip() for c in cells]

                # Skip header or empty rows
                if not any(texts):
                    continue
                if any(word in " ".join(texts).lower() for word in ["version", "release", "end of life", "eol", "support"]):
                    continue

                version, release_date, eol_date = self._normalize_row(texts)

                # XPath 2: first column contains name, version missing → shift and use "-" as placeholder
                if idx == 2 and i == 0:
                    software_name = version
                    continue  # skip placeholder row

                # XPath 9 & 11: handle same logic
                if idx in {9, 11} and special_first_value is None:
                    special_first_value = version
                    software_name = special_first_value
                    continue  # skip placeholder row

                if idx in {9, 11} and version == special_first_value:
                    software_name = special_first_value
                    version = "-"  # placeholder since no version exists

                # For XPath 2, also make version placeholder for all rows if missing
                if idx == 2 and not version:
                    version = "-"

                product = PaloAltoProduct(
                    software_name=software_name,
                    version=version,
                    release_date=release_date,
                    eol_date=eol_date
                )
                self.data.append(product.as_dict())

    def save_to_csv(self, filename="paloalto_software6.csv"):
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
