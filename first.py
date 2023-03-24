import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

userAgent = ("Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f'user-agent={userAgent}')
options.add_argument('--no-sandbox')
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

data = []
def getProducts():
    with open('amazon_bags.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Price', 'URL', 'Rating', 'Number of Reviews'])
        cnt = 1
        for count in range(1,21):
            print(f"\n--------> ON {cnt} <--------\n")
            template = f"https://www.amazon.in/s?k=bags&page={count}&crid=2M096C61O4MLT&qid=1679493286&sprefix=ba%2Caps%2C283&ref=sr_pg_{count}"
            driver.get(template)

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")))

            products = driver.find_elements(By.CSS_SELECTOR,"div[data-component-type='s-search-result']")
            for product in products:
                try:
                    name = product.find_element(By.CSS_SELECTOR,"h2 a").text
                except:
                    name = ""
                try:
                    url = product.find_element(By.CSS_SELECTOR,"h2 a").get_attribute("href")
                except:
                    url = ""
                try:
                    rating = product.find_element(By.CSS_SELECTOR,
                    "span.a-icon-alt").get_attribute("innerHTML")
                except:
                    rating = ""
                try:
                    num_reviews = product.find_element(By.CSS_SELECTOR,"span.a-size-base.s-underline-text").text.replace(' ', '').replace('(', '').replace(')', '')  
                except:
                    num_reviews = ""
                try:
                    price = product.find_element(By.CSS_SELECTOR,"span.a-price-whole").text
                except:
                    price = ""

                writer.writerow([name, price, url, rating, num_reviews])
            cnt = cnt+1

getProducts()