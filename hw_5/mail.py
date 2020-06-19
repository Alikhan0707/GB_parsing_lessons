from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('192.168.8.105', 27017)
db = client['emails_letters_db']

letters = db.letters

driver = webdriver.Chrome('/Users/macbook/Desktop/gb_data_parse/lesson_5/chromedriver')
driver.maximize_window()
driver.get('https://mail.ru')

login_elem_id = 'mailbox:login'
login = 'study.ai_172'

password_elem_id = 'mailbox:password'
password = 'NextPassword172'

contact_class_name = 'letter-contact'
date_class_name = 'letter__date'
subject_class_name = 'thread__subject-line'
body_class_name = 'letter__body'

assert 'Mail.ru' in driver.title


def enter_value(elem_id, value):

    btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, elem_id))
    )
    btn.send_keys(value)
    btn.send_keys(Keys.RETURN)


def full_text(contact_cn, date_cn, subject_cn, body_cn):

    letter = {}

    body = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, body_cn))
    )
    body = body.text

    subject = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, subject_cn))
    )
    subject = subject.text

    contact = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, contact_cn))
    )
    contact = contact.text

    date = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, date_cn))
    )
    date = date.text

    letter['contact'] = contact
    letter['date'] = date
    letter['subject'] = subject
    letter['body'] = body

    letters.update_one(letter, {'$set': letter}, upsert=True)

    btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'portal-menu-element_next'))
    )
    btn.click()


enter_value(login_elem_id, login)
enter_value(password_elem_id, password)
button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'js-letter-list-item'))
    )
button.click()

while EC.element_to_be_clickable((By.CLASS_NAME, 'portal-menu-element_next')):
    full_text(contact_class_name,date_class_name, subject_class_name, body_class_name)


