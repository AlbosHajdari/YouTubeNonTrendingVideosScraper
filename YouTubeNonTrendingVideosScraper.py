import time, clipboard, requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

df = pd.DataFrame(columns = ['id', 'published_At', 'videot_title', 'description', 'thumbnail_url',
                             'channel_Title', 'category_Id', 'trending', 'date_registered'])


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
    print("IDS = " + str(IDs))
    return IDs

def get_string_param_IDs(IDs):
    print("Start of get_string_param_IDs")
    total = len(IDs)
    groupsOf50 = int(total/50)
    for g in range(0,groupsOf50):
        splitInGroupsOf50(g*50,g*50+50)
    splitInGroupsOf50(groupsOf50*50,total)
    print("End of get_string_param_IDs")
    #return stringParamIDs

def splitInGroupsOf50(beginning, end):
    print("Start of splitInGroupsOf50")
    stringParamIDs = ""
    for i in range(beginning,end):
        stringParamIDs = stringParamIDs+str(IDs[i]) +","
    stringParamIDs = stringParamIDs[:-1]
    data = getData(stringParamIDs,apiKey)
    addData(data)
    print("End of splitInGroupsOf50")

def getData(stringParamIDs, apiKey):
    print("Start of getData")
    # Builds the URL and requests the JSON from it
    request_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={stringParamIDs}&key={apiKey}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    items = request.json().get('items')
    print("ITEMS = " + str(items))
    print("End of getData")
    return items

def addData(data):
    print("Start of addData")
    global df
    for line in data:
        df = df.append({'id' : line['id'], 
                        'published_At' : line['snippet']['publishedAt'], 
                        'videot_title' : line['snippet']['title'],  
                        'description' : line['snippet']['description'],  
                        'thumbnail_url' : line['snippet']['thumbnails']['default']['url'],  
                        'channel_Title' : line['snippet']['channelTitle'],  
                        'category_Id' : line['snippet']['categoryId'],
                        'trending' : 'false',
                        'date_registered' : time.strftime("%d.%m.%Y")},
                ignore_index = True)
    print("End of addData")

if __name__ == "__main__":
    apiKey = ""
    countriesList = ["AU"]#, "CA", "IE", "JM", "MT", "NZ", "GB", "US"]
    for country in countriesList:
        print("COUNTRY = " +country)
        driver_get_and_scroll(country)
        IDs = get_IDs()
        #del IDs[-1] #the attribute of the last element is NONE because it doesn't belong to a video item/element, so I removed it
        get_string_param_IDs(IDs)
        df.to_csv(country+"_"+time.strftime("%d.%m.%Y")+".csv")
