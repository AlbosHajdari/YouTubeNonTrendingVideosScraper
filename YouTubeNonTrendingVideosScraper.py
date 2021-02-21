import time, clipboard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

def driver_get_and_scroll(country):
    driver.get("https://www.youtube.com/?gl="+country)

    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("DONE SCROLLING")

def get_IDs():
    user_data = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
    IDs = []
    for i in user_data:
                attribute = str(i.get_attribute('href'))
                attribute = attribute.replace('https://www.youtube.com/watch?v=', '')  #get only the IDs
                if attribute!="None":
                    IDs.append(attribute)
    return IDs

def get_string_param_IDs(IDs):
    stringParamIDs = ""
    for id in IDs:
        stringParamIDs = stringParamIDs + str(id) + ","
    stringParamIDs = stringParamIDs[:-1]
    return stringParamIDs

if __name__ == "__main__":
    countriesList = ["AU"]#, "CA", "IE", "JM", "MT", "NZ", "GB", "US"]
    for country in countriesList:
        print("COUNTRY = " +country)
        driver_get_and_scroll(country)
        IDs = get_IDs()
        del IDs[-1] #the attribute of the last element is NONE because it doesn't belong to a video item/element, so I removed it
        total = len(IDs)
        groupsOf50 = int(total/50)
        for g in range(0,groupsOf50):
            stringParamIDs = ""
            for i in range(g*50,g*50+50):
                stringParamIDs = stringParamIDs+str(IDs[i]) +","
            stringParamIDs = stringParamIDs[:-1]
            print("Size = " + str(len(stringParamIDs)))
            print("Grupa = " + stringParamIDs)
            #getData(stringParamIDs)
            #addData(getData)
        stringParamIDs = ""
        for i in range(groupsOf50*50,total):
            stringParamIDs = stringParamIDs+str(IDs[i]) +","
        stringParamIDs = stringParamIDs[:-1]
        print("Size = " + str(len(stringParamIDs)))
        print("Grupa = " + stringParamIDs)
        #getData(stringParamIDs)
        #addData(getData)

        #stringParamIDs = get_string_param_IDs(IDs)
        #print (stringParamIDs)
        #clipboard.copy(stringParamIDs)

