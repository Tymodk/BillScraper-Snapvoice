from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

user = "tymo@productbuilder.ai"
pwd = "Scrape123"

driver = webdriver.Firefox(executable_path='C:/Users/tymo.dekock/Documents/Stage/Gecko/geckodriver.exe')

driver.get("https://cloud.digitalocean.com/login")
assert "DigitalOcean" in driver.title
elem = driver.find_element_by_id("user_email")
for i in range(0, len(user)):
    elem.send_keys(user[i])
    time.sleep(0.25)
elem = driver.find_element_by_id("user_password")
for i in range(0, len(pwd)):
    elem.send_keys(pwd[i])
    time.sleep(0.25)
elem.send_keys(Keys.RETURN)
time.sleep(30)
driver.get("https://cloud.digitalocean.com/account/billing")
time.sleep(10)
assert "DigitalOcean - Account" in driver.title
print(driver.current_url)
elem = driver.find_element_by_xpath("//td[@class='invoice']/a")
elem.click()
time.sleep(3)
print(driver.current_url)

elem = driver.find_element_by_class_name("Button--blue")
elem.click()
time.sleep(0.5)
print(driver.current_url)

elem = driver.find_element_by_partial_link_text("PDF").get_attribute("href")
requesturl = elem
print(elem)
driver.get(elem)
print(driver.current_url)
elem = driver.find_element_by_id("download")
elem.click()

# TODO: Figure out a way to download pdfs
# Try requests with cookies we got from seleniums