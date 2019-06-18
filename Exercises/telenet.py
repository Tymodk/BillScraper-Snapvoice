from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from os import path, getcwd
import os
import uuid
from base64 import b64decode
from Crypto.Cipher import AES

def scrapeTelenet(user, pwd, userId, key):
    id = str(uuid.uuid4())
    base_dir= getcwd() + '\\invoices\\telenet\\' + id + '\\'
    print(base_dir)
    iv = 'asdfasdfasdfasdf'
    encoded = b64decode(pwd)
    dec = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    value = dec.decrypt(encoded)
    pwd = str(value.decode("utf-8")).replace('╗', '').replace('╔', '').replace('','').replace('', '').replace('', '').replace('', '')
    print(pwd)
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
    driver.get('https://www2.telenet.be/nl')
    time.sleep(3)
    elem = driver.find_element_by_class_name('Button--login-header')
    elem.click()
    time.sleep(3)
    elem = driver.find_element_by_id("j_username")
    for i in range(0, len(user)):
        elem.send_keys(user[i])
        time.sleep(0.15)
    elem = driver.find_element_by_id("j_password")
    for i in range(0, len(pwd)):
        elem.send_keys(pwd[i])
        time.sleep(0.15)
    elem = driver.find_element_by_class_name("login_btn")
    time.sleep(35)
    elem.click()
    driver.get('https://www2.telenet.be/content/www-telenet-be/nl/klantenservice/raadpleeg-je-aanrekening')
    time.sleep(3)
    try:
        driver.find_element_by_class_name("upc_button").click()
        time.sleep(1)
    except:
        print('no overlay')
    
    elems = driver.find_elements_by_class_name("pdficon")
    for elem in elems:
        elem.click()
        count += 1
        time.sleep(1)
    time.sleep(3)
    driver.close()
    print('trying to access filenames')
    print(base_dir)
    filenames = os.listdir(base_dir)
    for i in range(0,count):
        os.rename(base_dir+ filenames[i], base_dir+filenames[i] + ".pdf")
    filenames = os.listdir(base_dir)

    multi_files = {}
    for i in range(0, count):
        location = base_dir+filenames[i]
        print(location)
        multi_files['file'+str(i+1)] = open(location, 'rb')
        #onefile =open(location, 'rb')
        
    requests.post('http://localhost:8080/files/pdfstore', files=multi_files, data={'userId': userId, 'Platform': 'Telenet'})
