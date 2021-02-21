import time, clipboard, requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


#driver = webdriver.Firefox()

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
    total = len(IDs)
    groupsOf50 = int(total/50)
    for g in range(0,groupsOf50):
        splitInGroupsOf50(g*50,g*50+50)
    splitInGroupsOf50(groupsOf50*50,total)
    #return stringParamIDs

def splitInGroupsOf50(beginning, end):
    stringParamIDs = ""
    for i in range(beginning,end):
        stringParamIDs = stringParamIDs+str(IDs[i]) +","
    stringParamIDs = stringParamIDs[:-1]
    print("Size = " + str(len(stringParamIDs)))
    print("Grupa = " + stringParamIDs)
    #getData(stringParamIDs)
    #addData(getData)

def getData(stringParamIDs, apiKey):
    # Builds the URL and requests the JSON from it
    request_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={stringParamIDs}&key={apiKey}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    items = request.json().get('items')
    return items
    #return data

if __name__ == "__main__":
    #countriesList = ["AU"]#, "CA", "IE", "JM", "MT", "NZ", "GB", "US"]
    #for country in countriesList:
    #    print("COUNTRY = " +country)
    #    driver_get_and_scroll(country)
    #    IDs = get_IDs()
    #    #del IDs[-1] #the attribute of the last element is NONE because it doesn't belong to a video item/element, so I removed it
    #    get_string_param_IDs(IDs)
    stringParamIDs = "y_bwKW6V1lw,5qap5aO4i9A"
    apiKey = "AIzaSyCWhAzyPoNV74327R60On43KOEckztmUpI"
    data = getData(stringParamIDs,apiKey)
    df = pd.DataFrame(columns = ['id', 'publishedAt', 'videot_title', 'description',
                                 'thumbnail_url', 'channelTitle', 'categoryId'])
    for line in data:
        df = df.append({'id' : line['id'], 
                        'publishedAt' : line['snippet']['publishedAt'], 
                        'videot_title' : line['snippet']['title'],  
                        'description' : line['snippet']['description'],  
                        'thumbnail_url' : line['snippet']['thumbnails']['maxres']['url'],  
                        'channelTitle' : line['snippet']['channelTitle'],  
                        'categoryId' : line['snippet']['categoryId']},
                ignore_index = True)
    print(df)
    df.to_csv('file_name.csv')