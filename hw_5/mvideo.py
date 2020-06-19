from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('192.168.8.105', 27017)
db = client['products_db']
sale_hits = db.sale_hits

driver = webdriver.Chrome('/Users/macbook/Desktop/gb_data_parse/lesson_5/chromedriver')
driver.maximize_window()
driver.get('https://www.mvideo.ru/')
time.sleep(10)
next_button_class_name = 'next-btn'
sel_hits = 'sel-hits-block '
sel_hits_block = driver.find_elements_by_class_name(sel_hits)[1]
action = ActionChains(driver)
action.move_to_element(sel_hits_block).perform()
hits_block = sel_hits_block.find_element_by_class_name('accessories-carousel-wrapper')
next_button = hits_block.find_element_by_class_name(next_button_class_name)

while next_button.is_displayed():
    if next_button.is_enabled():
        next_button.click()

hits_block = sel_hits_block.find_element_by_class_name('accessories-product-list')
elems = hits_block.find_elements_by_tag_name('li')

for elem in elems:

    product = {}
    bonus = elem.find_element_by_class_name('tooltipstered').text
    rate = elem.find_element_by_class_name('c-star-rating_reviews-qty').text
    title = elem.find_element_by_tag_name('h4').get_attribute('title')
    price = elem.find_element_by_class_name('c-pdp-price__current').text

    product['title'] = title
    product['rate'] = rate
    product['price'] = price
    product['bonus'] = bonus

    sale_hits.update_one(product, {'$set': product}, upsert=True)

for i in sale_hits.find({}):
    pprint(i)

