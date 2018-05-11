# -*- coding: utf-8 -*-
import csv
import StringIO
import requests
import pdb
from bs4 import BeautifulSoup, SoupStrainer
import itertools
from itertools import izip_longest
#from itertools import zip_longest

#url = "http://www.cn411.ca/main02view04.aspx?LinkTreeID=S020907&PageSize=100&PageID=1&AreaID=416"
#
#r = requests.get(url)
#soup = BeautifulSoup(r.content)

#pages = soup.find("span",{"id":"ctl00_cphRight_Main0102view_1_lbPager"})
#lastPage = str(pages)[-9:-7]

#g_data = soup.find("table",{"id":"ctl00_cphRight_Main0102view_1_DataList1"})

#pageNum = 0

def scrapeMainPage(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    g_data = soup.find("table",{"id":"ctl00_cphRight_Main0102view_1_DataList1"})

    pageNum = 0
    while g_data is not None:
        pageNum = pageNum + 1
        url = url[:-12] + str(pageNum) + "&AreaID=416"
        print url
        #url = "http://www.cn411.ca/main02view04.aspx?LinkTreeID=S020131&PageSize=100&PageID=" + str(pageNum)
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        g_data = soup.find("table",{"id":"ctl00_cphRight_Main0102view_1_DataList1"})

        names = g_data.find_all("a",{"class":"tree12"})
        contacts = g_data.find_all("span",{"class":"T12"})
        hyperLinks = g_data.find_all("a")

        numberList = []
        nameList = []
        ratingList = []
        addressList =[]
        postalCodeList = []

        data = [nameList,numberList,ratingList,addressList,postalCodeList]

        for name in names:
            name = name.text.encode('utf8')
            nameList.append(name)

        for link in hyperLinks:
            locationData = scrapeInnerPage(url[0:20] + link["href"])
            addressList.append(locationData[0])
            postalCodeList.append(locationData[1])
            #print url[0:20] + link["href"]

        for item in g_data:
            try:
                phoneNum = item.contents[1].find_all("span",{"class":"T12"})[1].text.encode('utf8')
                numberList.append(phoneNum)

            except:
                pass

        for item in g_data:
            try:
                rating = item.contents[1].find_all("span",{"class":"T12"})[2].text.encode('utf8')
                ratingList.append(rating[30:len(rating)])
            except:
                pass

        export_data = izip_longest(*data, fillvalue = '')

        with open('data.csv','a') as file:
            writer = csv.writer(file)
            #writer.writerow(("nameList","numberList","ratingList"))
            writer.writerows(export_data)


def scrapeInnerPage(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    addressData = soup.find("span",{"id":"ctl00_cphLeft_Views1_txtLinkAddress"})
    addressDataM = soup.find("span",{"id":"ctl00_cphLeft_Viewms1_txtLinkAddress"})
    postalCodeData = soup.find("span",{"id":"ctl00_cphLeft_Views1_txtLinkPostalCode"})
    postalCodeDataM = soup.find("span",{"id":"ctl00_cphLeft_Viewms1_txtLinkPostalCode"})

    if addressData is not None:
        address = addressData.text.encode('utf8')
    elif addressDataM is not None:
        address = addressDataM.text.encode('utf8')
    else:
        address = 'N/A'

    if postalCodeData is not None:
        postalCode = postalCodeData.text.encode('utf8')
    elif postalCodeDataM is not None:
        postalCode = postalCodeDataM.text.encode('utf8')
    else:
        postalCode = 'N/A'


    print address
    return [address, postalCode]


scrapeMainPage\
("http://www.cn411.ca/main02view04.aspx?LinkTreeID=S020101&PageSize=100&PageID=1&AreaID=416")
