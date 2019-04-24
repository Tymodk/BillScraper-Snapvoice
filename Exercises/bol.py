from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from os import path, getcwd
from dotenv import load_dotenv
load_dotenv()
import os


base_dir= getcwd() + '\\invoices\\bol.com\\'
print(base_dir)
user = os.getenv("BOLUSER")
pwd = os.getenv("BOLPASSWORD")

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

def scrapeBol(user, pwd):
    driver = webdriver.Firefox(firefox_profile=profile, executable_path='C:/Users/tymo.dekock/Documents/Stage/Gecko/geckodriver.exe')
    driver.get('https://www.bol.com/nl/')
    time.sleep(3)
    assert "bol.com | de winkel van ons allemaal" in driver.title
    try:
        elem = driver.find_element_by_class_name("js_close_modal_window")
        elem.click()
    except:
        print("no overlay")
    time.sleep(2)
    elem = driver.find_element_by_class_name("account-button")
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_id("login_email")
    for i in range(0, len(user)):
        elem.send_keys(user[i])
        time.sleep(0.25)
    elem = driver.find_element_by_id("login_password")
    for i in range(0, len(pwd)):
        elem.send_keys(pwd[i])
        time.sleep(0.25)
    elem = driver.find_element_by_class_name("c-btn-primary--large")
    elem.click()
    driver.get('https://www.bol.com/nl/rnwy/account/facturen')

    elems = driver.find_elements_by_class_name('sb-pdf')
    for elem in elems:
        elem.click()
        time.sleep(1)

