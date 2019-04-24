from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from os import path, getcwd
from dotenv import load_dotenv
load_dotenv()
import os


base_dir= getcwd() + '\\invoices\\coolblue\\'
print(base_dir)
user = os.getenv("COOLUSER")
pwd = os.getenv("COOLPASSWORD")

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

def scrapeCool(user, pwd):
    driver = webdriver.Firefox(firefox_profile=profile, executable_path='C:/Users/tymo.dekock/Documents/Stage/Gecko/geckodriver.exe')
    driver.get('https://www.coolblue.be/nl/inloggen')
    time.sleep(3)
    assert "Inloggen - Coolblue - alles voor een glimlach" in driver.title

    elem = driver.find_element_by_id("login_page_emailaddress")
    for i in range(0, len(user)):
        elem.send_keys(user[i])
        time.sleep(0.25)
    elem = driver.find_element_by_id("login_page_password")
    for i in range(0, len(pwd)):
        elem.send_keys(pwd[i])
        time.sleep(0.25)
    elems = driver.find_elements_by_class_name("button--order")
    elems[1].click()

    driver.get('https://www.coolblue.be/nl/mijn-coolblue-account/orderoverzicht')
    time.sleep(1)
    assert "Mijn bestellingen - Coolblue - alles voor een glimlach" in driver.title

    while 1:
        try:
            elems = driver.find_elements_by_class_name("order-row")
            for elem in elems:
                elem.click()
                time.sleep(5)
                modalelem = driver.find_element_by_partial_link_text("Factuur")
                modalelem.click()
                modalelem.send_keys(Keys.ESCAPE)
            next = driver.find_element_by_partial_link_text("Volgende")
            next.click()
            time.sleep(5)
        except:
            print('Closing...')
            driver.close()



