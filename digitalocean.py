from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from os import path, getcwd

import requests


base_dir= getcwd() + '\\invoices\\'
print(base_dir)
user = "tymo@productbuilder.ai"
pwd = "Scrape123"

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


cookies = driver.get_cookies()

driver.get(elem)
time.sleep(0.7)
elem = driver.find_element_by_id("download")
elem.click()


'''
s = requests.Session()

for cookie in cookies:
    print(cookie)
    try:
        s.cookies.set(cookie['name'], cookie['value'], path=cookie['path'], domain=cookie['domain'], secure=cookie['secure'], expires=cookie['expiry'])
    except KeyError:
        s.cookies.set(cookie['name'], cookie['value'], path=cookie['path'], domain=cookie['domain'], secure=cookie['secure'])

print(s.cookies)
response = s.get(requesturl)
with open(base_dir+ 'oceanInvoice.pdf', 'wb') as pdf:
    pdf.write(response.content)

# soup = BeautifulSoup(content)
# print(soup)

# TODO: Figure out a way to download pdfs
# Try requests with cookies we got from seleniums
'''