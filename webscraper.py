from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import pandas as pd
import os
import time
from selenium.common.exceptions import NoSuchElementException

total = []
#set executable path
driver = webdriver.Chrome(executable_path='/Users/kasho/Documents/chromedriver.exe')
driver.implicitly_wait(30)
pages = 3

for page in range(1, pages+1):
    url = "https://ascentoutdoors.com/collections/sale-items?page="+ str(page)
    driver.get(url)

    products = driver.find_elements_by_class_name("spf-product-card__template-1")
    for i in range(len(products)):
        #driver.back() resets products list, so products must be reset at the beginning of each iteration
        products = driver.find_elements_by_class_name("spf-product-card__template-1")
        product = products[i]

        #set discount rate (not all products have discount rates)
        try:
            discount_rate = product.find_element_by_class_name('spf-product__label-sale').text
        except NoSuchElementException:
            discount_rate = "No Discount"
        
        #set individual product page link
        product_page_element = product.find_element_by_class_name('spf-product-card__image-wrapper')
        individual_product_page = product_page_element.get_attribute('href')

        #click on the product to get the rest of the information
        product_page_element.click()

        #set listing title
        listing_title = driver.find_element_by_css_selector('h1.product-item-caption-title').text
        
        #set sale price (there are multiple elements with the relevant id)
        #not all products are on sale
        try:
            sale_price_list = driver.find_elements_by_id('ComparePrice-product-template')
            sale_price = sale_price_list[1].text
        except (NoSuchElementException, IndexError):
            sale_price = "Not On Sale"
        except IndexError:
            sale_price = "Not On Sale"

        #set retail price (there are multiple elements with the relevant id)
        retail_price_list = driver.find_elements_by_id('ProductPrice-product-template')
        retail_price = retail_price_list[1].text
        
        #set description (description HTML is formatted different for each product)
        #currently only compiles HTML descriptions formatted according to xpath below
        try:
            description = driver.find_element_by_xpath("//div[@class = 'product-item-caption-desc']/div[1]/p/span[1]").text
        except NoSuchElementException:
            description = "No Description"

        #set item sku
        item_sku = driver.find_element_by_class_name('variant-sku-product-template').text
        
        #set review rating (there are multiple elements with the relevant class)
        review_rating_list = driver.find_elements_by_class_name('spr-badge-caption')
        review_rating = review_rating_list[1].text

        #set item image link
        item_image_link = driver.find_element_by_class_name('product-item-img').get_attribute('src')
        
        #go back to the original screen
        driver.execute_script("window.history.go(-1)")
        new_product = ((individual_product_page,listing_title,sale_price,discount_rate,retail_price,
        description,item_sku,review_rating,item_image_link))
        total.append(new_product)

driver.close()
df = pd.DataFrame(total,columns=['Individual Product','Listing Title','Sale Price','Discount Rate','Retail Price',
'Description','Item Sku','Review Rating','Item Image Link'])
df.to_csv('ascentsale.csv')