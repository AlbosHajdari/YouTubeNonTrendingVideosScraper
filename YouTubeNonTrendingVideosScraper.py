import requests#, clipboard, time
from bs4 import BeautifulSoup
import pandas as pd


def api_request(parameter):
    request_url = f"https://www.youtube.com/?gl={parameter}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    return request.text



if __name__ == "__main__":

    htmlSourceCode = api_request("US")
    soup = BeautifulSoup(htmlSourceCode)
    #clipboard.copy(str(soup))
    text1 = str(soup).split("url\":\"/watch?v=")

    for i in range(1,len(text1),1):
        text2 = text1[i].split("\",\"",1)[0]
        print(i)
        print(text2)
        #time.sleep(.05)


    #dataSet = pd.read_csv('originalData.csv')

    #dataSet.to_csv('updatedData.csv')

    #lista = getIdsList()
    #data = get_data(lista)
    #writeDataToFile(data)