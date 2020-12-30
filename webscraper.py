from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
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

    products = driver.find_elements_by_class_name("spf-product-card__template-1")
    for product in products:
        discount_rate = product.find_element_by_class_name('spf-product__label-sale').text
        # product_page_element = product.find_element_by_class_name('spf-product-card__image-wrapper')
        # individual_product_page_url = product_page_element.get_attribute('href')
        # #click on the product to get the rest of the information
        # product_page_element.click()
        # listing_title = product.find_element_by_class_name('product-item-caption-title').text
        # sale_price = product.find_element_by_xpath("//li[@id = 'ComparePrice-product-template']/span").text
        # retail_price = product.find_element_by_xpath("//li[@id = 'ProductPrice-product-template']/span").text
        # description = product.find_element_by_xpath("//div[@class = 'main-product-description-product-template']/p/span").text
        # item_skus = product.find_element_by_class_name('variant-sku-product-template').text
        # review_rating = product.find_element_by_class_name('spr-badge-caption').text
        # item_image_link = product.find_element_by_class_name('product-item-img').get_attribute(src)
        # #go back to the original screen
        # driver.back()
        # driver.implicitly_wait(30)
        new_product = ((discount_rate))
        total.append(product)

driver.close()
df = pd.DataFrame(total,columns=['Discount Rate'])
df.to_csv('ascentsale.csv')