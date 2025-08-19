What is web Scraping?  
Web scraping is the process of automatically extracting data from websites. Instead of manually copying information from web pages, web scraping uses scripts or tools to collect data in a structured format, such as tables, lists, or text files. This helps in saving time, reducing errors, and handling large volumes of data efficiently.

Requirements for web scraping:  
Selenium  
Web Driver  
VS Code

Steps to perform to run this files:  
1. Install selenium in VS code.  
   Command: pip install selenium

2. Install a compatible driver for your browser.  
   Ex. If Chrome (Version 139.0.7258.128), then the chromedriver has  
   version(139.x.xxxx.xxx).

3. Copy the Python file.  
   Note: Chnage the browser-driver's url with your url.

4. You can even add website of your choice to scrap by changing web url, changing Xpath, and defining proper regex.

Task 1: In this task i have scraped the "https://en.wikipedia.org/wiki/List_of_tallest_buildings" and extracted the "Name" and "City" column from it.  
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/ScrapTask1.py)  
[View Output](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/ScrapTask1_output.csv)  

Task 2: In this task i have scraped the "https://en.wikipedia.org/wiki/List_of_sovereign_states_in_Europe_by_GDP_(nominal)" and extracted the "Country" and "GDP 2025" columns from it.  
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/ScrapTask2.py)  
[View Output](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/ScrapTask2_output.csv)  

Task 3: In this task i have scraped the "https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944" and extracted the Vendor, Product Name, model, Description, Product URL, Cost columns from it.  
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/webscrapingtask(troemner).py)
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/troemner_products.csv)

Task 4: In this task i have scraped the "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates" and extracted the Vendor Name, Product Name, EOL Date, resource, Recommended Replacement columns from it.  
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/PaloAlto(Hardware).py)
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/PaloAlto(Hardware).csv)

Task 5: In this task i have scraped the "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary" and extracted the Software Name,  version, EOL Date, EOL Date, Release Date columns from it. 
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/PaloAlto(Software).py)
[View File](https://github.com/pornimarahane/ApexaiQ-Internship-tasks-Pornima/blob/main/Web-Scrapping/PaloAlto(Software).csv)






