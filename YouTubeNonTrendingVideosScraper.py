import time, clipboard, requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()
apiKey = ""
df = pd.DataFrame(columns = ['id', 'published_At', 'videot_title', 'description', 'thumbnail_url',
                             'channel_Title', 'category_Id', 'trending', 'date_registered'])


def driver_get_and_scroll(country):
    driver.get("https://www.youtube.com/?gl="+country)

    SCROLL_PAUSE_TIME = 2

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

def get_nonTrendingIDs():
    user_data = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
    IDs = []
    for i in user_data:
                attribute = str(i.get_attribute('href'))
                attribute = attribute.replace('https://www.youtube.com/watch?v=', '')  #get only the IDs
                if attribute!="None":
                    IDs.append(attribute)
    return IDs

def get_AllNonTrendingData(IDs):
    print("Start of get_AllNonTrendingData")
    total = len(IDs)
    groupsOf50 = int(total/50)
    for g in range(0,groupsOf50):
        get_NonTrendingRowsInGroupsOf50(g*50,g*50+50)
    get_NonTrendingRowsInGroupsOf50(groupsOf50*50,total)
    print("End of get_AllNonTrendingData")
    #return stringParamIDs

def get_NonTrendingRowsInGroupsOf50(beginning, end):
    print("Start of get_NonTrendingRowsInGroupsOf50")
    stringParamIDs = ""
    for i in range(beginning,end):
        stringParamIDs = stringParamIDs+str(nonTrendingIDs[i]) +","
    stringParamIDs = stringParamIDs[:-1]
    data = get_NonTrendingDataFromAPIrequest(stringParamIDs)
    update_DataFrame(data, False)
    print("End of get_NonTrendingRowsInGroupsOf50")

def get_NonTrendingDataFromAPIrequest(stringParamIDs):
    global apiKey
    print("Start of get_NonTrendingDataFromAPIrequest")
    # Builds the URL and requests the JSON from it
    request_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={stringParamIDs}&key={apiKey}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    items = request.json().get('items')
    if items is None:
        print(str(items))
    print("End of get_NonTrendingDataFromAPIrequest")
    return items

def update_DataFrame(data, trendingOrNotTrending):
    print("Start of update_DataFrame")
    global df
    for line in data:
        df = df.append({'id' : line['id'], 
                        'published_At' : line['snippet']['publishedAt'], 
                        'videot_title' : line['snippet']['title'],  
                        'description' : line['snippet']['description'],  
                        'thumbnail_url' : line['snippet']['thumbnails']['default']['url'],  
                        'channel_Title' : line['snippet']['channelTitle'],  
                        'category_Id' : line['snippet']['categoryId'],
                        'trending' : trendingOrNotTrending,
                        'date_registered' : time.strftime("%d.%m.%Y")},
                ignore_index = True)
    print("End of update_DataFrame")

def get_TrendingDataFromAPIrequest(country, nextPageToken):
    global apiKey
    print("Start of get_TrendingDataFromAPIrequest")
    # Builds the URL and requests the JSON from it
    if(nextPageToken==""):
        request_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&maxResults=50&regionCode={country}&key={apiKey}"
    else:
        request_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&maxResults=50&pageToken={nextPageToken}&regionCode={country}&key={apiKey}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    items = request.json().get('items')
    if "nextPageToken" in request.json():
        nextPageToken = request.json().get('nextPageToken')
    else:
        nextPageToken = "doesNotExist"
    if items is None:
        print(str(items))
    print("End of get_TrendingDataFromAPIrequest")
    return items, nextPageToken

def get_TrendingRowsInGroupsOf50(country):
    nextPageToken = ""

    while(nextPageToken!="doesNotExist"):
        data = get_TrendingDataFromAPIrequest(country, nextPageToken);
        nextPageToken = data[1]
        update_DataFrame(data[0], True)

if __name__ == "__main__":
    countriesList = ["US", "CA", "JM", "AU", "NZ", "GB", "IE", "MT"]#,, , 
    for country in countriesList:
        print("COUNTRY = " +country)
        ### Start of TRENDING ###
        get_TrendingRowsInGroupsOf50(country)
        ### End of TRENDING ###

        ### Start of NON-TRENDING ###
        driver_get_and_scroll(country)
        nonTrendingIDs = get_nonTrendingIDs()
        get_AllNonTrendingData(nonTrendingIDs)
        ### End of NON-TRENDING ###
        df = df.drop_duplicates(subset=['id'])
        
        df.to_csv(country+"_"+time.strftime("%d.%m.%Y")+".csv")
        df = pd.DataFrame(columns=df.columns)
