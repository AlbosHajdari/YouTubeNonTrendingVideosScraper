import time
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
                IDs.append(attribute)
    return IDs

if __name__ == "__main__":
    driver_get_and_scroll("US")
    IDs = get_IDs()
    del IDs[-1] #the attribute of the last element is NONE because it doesn't belong to a video item/element, so I removed it
    
    
    i=1
    for id in IDs:
        print(i)
        print(id)
        i = i+1