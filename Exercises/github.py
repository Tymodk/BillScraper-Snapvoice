from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from os import path, getcwd
import os
import uuid
from base64 import b64decode
from Crypto.Cipher import AES

def scrapeGit(user, pwd, userId, key):
    id = str(uuid.uuid4())
    base_dir= getcwd() + '\\invoices\\github\\' + id + '\\'
    print(base_dir)
    iv = 'asdfasdfasdfasdf'
    encoded = b64decode(pwd)
    dec = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    value = dec.decrypt(encoded)
    pwd = str(value.decode("utf-8")).replace('╗', '').replace('╔', '').replace('','').replace('', '').replace('', '').replace('', '')

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
    driver.get('https://github.com/login')
    time.sleep(3)
    assert "Sign in to GitHub · GitHub" in driver.title    
    elem = driver.find_element_by_id("login_field")
    for i in range(0, len(user)):
        elem.send_keys(user[i])
        time.sleep(0.15)
    elem = driver.find_element_by_id("password")
    for i in range(0, len(pwd)):
        elem.send_keys(pwd[i])
        time.sleep(0.15)
    elem = driver.find_element_by_class_name("btn-primary")
    elem.click()
    driver.get('https://github.com/settings/organizations')
    elems = driver.find_elements_by_xpath('//strong[@class="ml-1"]')
    orgs = []
    for elem in elems:
        orgs.append(elem.text)

    for org in orgs:
         driver.get('https://github.com/organizations/'+ org + '/billing/history')
         try:
            time.sleep(1)
            assert "Payment history" in driver.title
            elemstwo = driver.find_elements_by_class_name('receipt')
            for elemtwo in elemstwo:
                elemtwo.click()
                count += 1
                time.sleep(0.5)
         except: 
            print('Not a biller in this org')
    driver.close()
    print('trying to access filenames')
    print(base_dir)
    filenames = os.listdir(base_dir)
    multi_files = {}
    for i in range(0, count):
        location = base_dir+filenames[i]
        print(location)
        multi_files['file'+str(i+1)] = open(location, 'rb')
        #onefile =open(location, 'rb')
        
    requests.post('http://localhost:8080/files/pdfstore', files=multi_files, data={'userId': userId, 'Platform': 'Github'})
