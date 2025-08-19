import re
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

        # 13 XPaths provided
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
        return "-"

    def _get_column_index(self, header_row, column_name):
        """Find index of a column by name in header row"""
        for idx, cell in enumerate(header_row.find_elements(By.TAG_NAME, "td")):
            if column_name.lower() in cell.text.lower():
                return idx
        return None

    def scrape(self):
        self.driver.get(self.url)
        time.sleep(3)

        for i, xp in enumerate(self.xpaths, start=1):
            try:
                table = self.driver.find_element(By.XPATH, xp)
            except:
                print(f"[!] Table not found for xpath: {xp}")
                continue

            # --- Get heading ---
            heading = "Unknown"
            for tag in ["h2", "h3", "b", "strong", "p"]:
                try:
                    heading = table.find_element(By.XPATH, f"./preceding-sibling::{tag}[1]").text.strip()
                    if heading:
                        break
                except:
                    continue

            # --- Handle rows ---
            rows = table.find_elements(By.XPATH, ".//tr")
            if not rows:
                continue

            header_cells = rows[0].find_elements(By.TAG_NAME, "td")
            header_texts = [c.text.strip().lower() for c in header_cells]

            # Identify column indices dynamically
            version_idx = None
            eol_idx = None
            release_idx = None
            for j, h in enumerate(header_texts):
                if "version" in h:
                    version_idx = j
                if "end" in h:
                    eol_idx = j
                if "release" in h:
                    release_idx = j
                if "standard support" in h:   # special case for panorama
                    eol_idx = j

            # Loop rows
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue

                # --- Default values ---
                product_name = heading
                version = "-"
                release_date = "-"
                eol_date = "-"

                # Handle special XPath cases by number
                if i == 1:  # Prisma Access Browser
                    product_name = "Prisma Access Browser"
                    version = cells[0].text.strip() if len(cells) > 0 else "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = cells[release_idx].text.strip() if release_idx is not None and len(cells) > release_idx else "-"

                elif i == 2:  # QRadar SaaS Products
                    product_name = "Threat Management (including QRadar)"
                    version = "-"
                    release_date = "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"

                elif i == 3:  # PAN-OS & Panorama
                    product_name = heading
                    version = cells[0].text.strip() if version_idx is not None and len(cells) > version_idx else "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = cells[release_idx].text.strip() if release_idx is not None and len(cells) > release_idx else "-"

                elif i == 4:  # Panorama Plugin
                    subtype = cells[0].text.strip()
                    product_name = f"{heading} - {subtype}"
                    version = cells[1].text.strip() if len(cells) > 1 else "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = cells[release_idx].text.strip() if release_idx is not None and len(cells) > release_idx else "-"

                elif i == 5:  # Traps ESM and Cortex
                    product_name = heading
                    version = cells[0].text.strip() if len(cells) > 0 else "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = cells[release_idx].text.strip() if release_idx is not None and len(cells) > release_idx else "-"

                elif i == 6:  # Cortex XSOAR (no release date)
                    product_name = heading
                    version = cells[0].text.strip() if len(cells) > 0 else "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = "-"

                elif i in [7, 8, 11]:  # GlobalProtect, Prisma Cloud Compute, CloudGenix
                    product_name = heading
                    version = cells[0].text.strip() if len(cells) > 0 else "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = cells[release_idx].text.strip() if release_idx is not None and len(cells) > release_idx else "-"

                elif i in [9, 12, 13]:  # Lightcyber Magna, Brightcloud, VM-Series
                    product_name = heading
                    version = "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = cells[release_idx].text.strip() if release_idx is not None and len(cells) > release_idx else "-"

                elif i == 10:  # Evident.io (no version but has release + eol)
                    product_name = heading
                    version = "-"
                    eol_date = cells[eol_idx].text.strip() if eol_idx is not None and len(cells) > eol_idx else "-"
                    release_date = cells[release_idx].text.strip() if release_idx is not None and len(cells) > release_idx else "-"

                # Normalize dates
                release_date = self._normalize_date(release_date)
                eol_date = self._normalize_date(eol_date)

                product = PaloAltoProduct(
                    software_name=product_name,
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
