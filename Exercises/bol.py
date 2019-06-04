from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from os import path, getcwd
import os
import uuid

def scrapeBol(user, pwd, userId):
    id = str(uuid.uuid4())
    base_dir= getcwd() + '\\invoices\\bol.com\\' + id + '\\'
    print(base_dir)


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
    count = 0
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
        time.sleep(0.15)
    elem = driver.find_element_by_id("login_password")
    for i in range(0, len(pwd)):
        elem.send_keys(pwd[i])
        time.sleep(0.15)
    elem = driver.find_element_by_class_name("c-btn-primary--large")
    elem.click()
    driver.get('https://www.bol.com/nl/rnwy/account/facturen')

    elems = driver.find_elements_by_class_name('sb-pdf')
    for elem in elems:
        elem.click()
        count += 1
        time.sleep(1)
    print('trying to access filenames')
    print(base_dir)
    filenames = os.listdir(base_dir)
    multi_files = {}
    for i in range(0, count):
        location = base_dir+filenames[i]
        print(location)
        multi_files['file'+str(i+1)] = open(location, 'rb')
        #onefile =open(location, 'rb')
        
    requests.post('http://localhost:8080/files/pdfstore', files=multi_files, data={'userId': userId, 'Platform': 'Bol.com'})
