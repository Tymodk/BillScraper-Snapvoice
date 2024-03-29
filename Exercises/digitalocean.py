from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from os import path, getcwd
from dotenv import load_dotenv
load_dotenv()
import os
from base64 import b64decode
from Crypto.Cipher import AES

base_dir= getcwd() + '\\invoices\\DigitalOcean\\'
print(base_dir)
user = os.getenv("OCEANUSER")
pwd = os.getenv("OCEANPASSWORD")

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.dir",base_dir)
profile.set_preference("browser.download.folderList",2)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")
profile.set_preference("browser.download.manager.showWhenStarting",False)
profile.set_preference("browser.helperApps.neverAsk.openFile","text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")
profile.set_preference("browser.helperApps.alwaysAsk.force", False)
profile.set_preference("browser.download.manager.useWindow", False)
profile.set_preference("browser.download.manager.focusWhenStarting", False)
profile.set_preference("browser.helperApps.neverAsk.openFile", "")
profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
profile.set_preference("browser.download.manager.showAlertOnComplete", False)
profile.set_preference("browser.download.manager.closeWhenDone", True)
profile.set_preference("pdfjs.disabled", True)


driver = webdriver.Firefox(firefox_profile=profile, executable_path='C:/Users/tymo.dekock/Documents/Stage/Gecko/geckodriver.exe')

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
elems = driver.find_elements_by_xpath("//td[@class='invoice']/a")
for i in range(0, len(elems)):
    elems = driver.find_elements_by_xpath("//td[@class='invoice']/a")
    elems[i].click()
    time.sleep(3)
    elem = driver.find_element_by_class_name("Button--blue")
    elem.click()
    time.sleep(0.5)
    elem = driver.find_element_by_partial_link_text("PDF")
    elem.click()
    driver.get("https://cloud.digitalocean.com/account/billing")
    time.sleep(10)
    assert "DigitalOcean - Account" in driver.title
driver.close()
