import csv
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

userAgent = ("Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('log-level=3')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-images')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f'user-agent={userAgent}')
options.add_argument('--no-sandbox')
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

with open(config.outputFile+'.csv', mode='r', encoding='ISO-8859-1') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    urls = [row['URL'] for row in csv_reader]
    data = []
    count = 1
    for url in urls:
        print(f"\n\tPage : {count}\n")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//body")))
        try:
            description = driver.find_element(By.ID, "productTitle").text.strip()
        except:
            continue
        try:
            asin = driver.find_element(By.XPATH, "//th[contains(text(),'ASIN')]/following-sibling::td").text.strip()
        except:
            asin = driver.find_element(By.XPATH, "//div[@id='detailBullets_feature_div']/ul[1]/li[4]/span[1]/span[2]").text.strip()
        try:
            product_description = driver.find_element(By.ID, "productDescription").text.strip()
        except:
            continue
        try:
            manufacturer = driver.find_element(By.XPATH, "//div[@id='detailBullets_feature_div']/ul[1]/li[3]/span[1]/span[2]").text.strip()
        except selenium.common.exceptions.NoSuchElementException:
            manufacturer = driver.find_element(By.XPATH, "(//td[@class='a-size-base prodDetAttrValue'])[2]").text.strip()
        except selenium.common.exceptions.NoSuchElementException:
            manufacturer = driver.find_element(By.XPATH, "//th[contains(text(),'Manufacturer')]/following-sibling::td").text.strip()

        scraped_data = {'Description': description, 'ASIN': asin,
                        'Product Description': product_description, 'Manufacturer': manufacturer}

        data.append(scraped_data)

        driver.switch_to.window(driver.window_handles[0])
        print("\nDESCRIPTION : ",description)
        print("\nASIN : ",asin)
        print("\nPRODUCT DESCRIPTION : ",product_description)
        print("\nMANUFACTURER : ",manufacturer)
        
        csv_second = open(config.outputFile+'_adv_scraped.csv', mode='w', encoding='utf-8', newline='')
        fieldnames = ['Description', 'ASIN', 'Product Description', 'Manufacturer']
        writer = csv.DictWriter(csv_second, fieldnames=scraped_data.keys())
                    
        writer.writeheader()
        for d in data:
            writer.writerow(d)
        count = count+1

