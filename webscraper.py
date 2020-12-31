from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

total = []
driver = webdriver.Chrome(executable_path='/Users/kasho/Documents/chromedriver.exe')
driver.implicitly_wait(30)
pages = 1
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

for page in range(1, pages+1):
    url = "https://ascentoutdoors.com/collections/sale-items?page="+ str(page)
    driver.get(url)
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)

    products = driver.find_elements_by_class_name("spf-product-card__template-1")
    for i in range(len(products)):
        products = driver.find_elements_by_class_name("spf-product-card__template-1")
        product = products[i]
        try:
            discount_rate = product.find_element_by_class_name('spf-product__label-sale').text
        except NoSuchElementException:
            discount_rate = "No Discount"
        product_page_element = product.find_element_by_class_name('spf-product-card__image-wrapper')
        individual_product_page = product_page_element.get_attribute('href')
        #click on the product to get the rest of the information
        product_page_element.click()
        listing_title = driver.find_element_by_css_selector('h1.product-item-caption-title').text
        try:
            sale_price = driver.find_element_by_xpath("//li[@id = 'ComparePrice-product-template']/span[@class= 'money]").text
        except NoSuchElementException:
            sale_price = "Not On Sale"
        retail_price = driver.find_element_by_xpath("//li[@id = 'ProductPrice-product-template']/span[@class = 'money']").text
        try:
            description = driver.find_element_by_xpath("//div[@class = 'product-item-caption-desc']/div[1]/p/span[1]").text
        except NoSuchElementException:
            description = "No Description"
        item_skus = driver.find_element_by_class_name('variant-sku-product-template').text
        review_rating = driver.find_element_by_class_name('spr-badge-caption').text
        item_image_link = driver.find_element_by_class_name('product-item-img').get_attribute(src)
        #go back to the original screen
        driver.execute_script("window.history.go(-1)")
        new_product = ((individual_product_page,listing_title,sale_price,discount_rate,retail_price,description))
        total.append(new_product)

driver.close()
df = pd.DataFrame(total,columns=['Individual Product','Listing Title','Sale Price','Discount Rate','Retail Price','Description'])
df.to_csv('ascentsale.csv')