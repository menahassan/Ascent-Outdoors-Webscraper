from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import pandas as pd
import os

total = []
driver = webdriver.Chrome(executable_path='/Users/kasho/Documents/chromedriver.exe')
#driver.implicitly_wait(30)
pages = 1

try:
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'spf-product-card__saleprice')))
except TimeoutException:
    print('Page timed out after 15 secs.')

for page in range(1, pages+1):
    url = "https://ascentoutdoors.com/collections/sale-items?page="+ str(page)
    driver.get(url)

    products = driver.find_elements_by_class_name("spf-product-card__template-1")
    for product in products:
        individual_product_page_url = product.find_element_by_class_name('spf-product-card__image-wrapper').get_attribute('href')
        item_image_url = product.find_element_by_class_name('spf-product-card__image').get_attribute('src')
        listing_title = product.find_element_by_css_selector('a.translatable').text
        sale_price = product.find_element_by_css_selector('span.spf-product-card__saleprice').text
        retail_price = product.find_element_by_class_name('spf-product-card__oldprice').text
        discount_rate = product.find_element_by_class_name('spf-product__label-sale').text
        #descriptions = product.find_element_by_class_name('')
        #item_skus = product.find_element_by_class_name('')
        review_rating = product.find_element_by_class_name('spr-badge-caption').text
        new_product = ((individual_product_page_url,item_image_url,listing_title,sale_price,retail_price,discount_rate,review_rating))
        total.append(product)

driver.close()
df = pd.DataFrame(total,columns=['Individual Product Page Link','Item Image Link','Listing Title','Sale Price','Retail Price','Discount Rate','Review Rating'])
df.to_csv('ascentsale.csv')