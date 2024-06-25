import json
import re
import os

import undetected_chromedriver as uc

from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

# Define the URL of the page to scrape
url = "https://www.shoprite.com/sm/delivery/rsid/166/past-purchases"


options = webdriver.ChromeOptions() 
options.headless = False
browser = uc.Chrome(options=options)
browser.get(url)

wait = WebDriverWait(browser, 10)

try:
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Sign In"]')))
    button.click()
except Exception as e:
    print(f"Button not found: {e}")

try:
    search_box = wait.until(EC.presence_of_element_located((By.ID, 'Email')))
    search_box.send_keys(os.environ.get("SHOPRITE_USERNAME"))
    search_box.send_keys(Keys.RETURN)
except Exception as e:
    print(f"Email input not found: {e}")

try:
    search_box = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    search_box.send_keys(os.environ.get("SHOPRITE_PASSWORD"))
    search_box.send_keys(Keys.RETURN)
except Exception as e:
    print(f"Password input not found: {e}")


WebDriverWait(browser, timeout=10).until(lambda d: d.find_element(By.ID, 'productGrid__title'))

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(browser.page_source, "html.parser")

# Find all product cards
product_cards = []

for i in range(1, 5):
    product_cards.append(soup.find_all(class_=re.compile('ProductCard--')))
    print(f"added products from page {i + 1}")
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{i + 1}']")))
        button.click()
        WebDriverWait(browser, timeout=10).until(lambda d: d.find_element(By.ID, 'productGrid__title'))
    except Exception as e:
        print(f"Button not found: {e}")

# Initialize an empty list to store product objects
products = []

# Iterate over each product card and extract relevant details
for page in product_cards:
    for card in page:
        try:
            # Extract the product name
            name = card.find(class_=re.compile('ProductCardNameWrapper')).text.strip().replace("Open Product Description", "")
            
            # Extract the product price
            price = card.find(class_=re.compile('ProductUnitPrice')).text.strip()
            
            # Extract the product SKU
            sku = card['data-testid'].split("-")[1]
            
            # Create a product dictionary
            product = {
                'name': name,
                'price': price,
                'sku': sku
            }
            
            # Add the product dictionary to the list
            products.append(product)
        except AttributeError:
            # Handle cases where some details might be missing
            continue

print(f"Fetched {len(products)} products.")

with open('products.json', 'w') as f:
    json.dump(products, f)