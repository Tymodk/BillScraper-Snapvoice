from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bson.objectid import ObjectId
from os import path, getcwd
from dotenv import load_dotenv
load_dotenv()
import os

import pymongo

base_dir= getcwd() + '\\invoices\\'

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['billboard']
eventsDB = db['paths']

result = eventsDB.find_one({"_id": ObjectId('5c9a4d523ace28df183cc0e7')})
url = result['path'][len(result['path'])-1]

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

driver.get(url['url'])
for i in range(0,(len(result['path'])-1)):
    nothingfound = 0
    time.sleep(5)
    step = result['path'][i]

    inputstep = 0
    try:
        print(step['input'])
        inputstep = 1
    except:
        inputstep = 0
    if(inputstep):
        elem = driver.find_element_by_id(step['id'])
        for i in range(0, len(step['valueofinput'])):
            elem.send_keys(step['valueofinput'][i])
            time.sleep(0.25)
    else:
        if(step['className'] == '' and step['id'] == '' and step['innertext'] == ''):
            elem.send_keys(Keys.RETURN)
        else:
            if (step['id'] != ''):
                elem = driver.find_element_by_id(step['id'])
            else:
                try:
                    elem = driver.find_element_by_xpath("//a[@class='"+ step['className'] +"']")
                except:
                    try:
                        elem = driver.find_element_by_xpath("//input[@class='"+ step['className'] +"']")
                    except:
                        try:
                            elem = driver.find_element_by_xpath("//span[@class='"+ step['className'] +"']")                  
                        except:
                            try: 
                                elem = driver.find_element_by_xpath("//div[@class='"+ step['className'] +"']")  
                            except:
                                nothingfound = 1
            if (nothingfound == 0):                
                elem.click()
