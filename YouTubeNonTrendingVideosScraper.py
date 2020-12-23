from bs4 import BeautifulSoup
import pandas as pd
import time



if __name__ == "__main__":

    f = open("htmlElements.txt", "r", encoding='UTF-8')
    text = f.read()
    text1 = str(text)
    text1 = text1.replace('\n', ' ').replace('\r', '').replace(' ', '')
    text1 = text1.split("href=\"/watch?v=");

    for i in range(1,len(text1),2):
        text2 = text1[i].split("\">",1)[0]
        print(int(i/2))
        print(text2)
        #time.sleep(.05)
        i=i+1


    #dataSet = pd.read_csv('originalData.csv'))

    #dataSet.to_csv('updatedData.csv')

    #lista = getIdsList()
    #data = get_data(lista)
    #writeDataToFile(data)