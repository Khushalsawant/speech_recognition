#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from textblob import TextBlob
import sys
import requests
import json

if sys.version_info >= (3,):
    import urllib.request as urllib2
else:
    import urllib2

word = 'business'

def Business_news(word):
    news_url = 'https://timesofindia.indiatimes.com/'+ word
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://cssspritegenerator.com',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    response = requests.get(news_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    divTag = soup.find_all("div", {"id": "c_0101"})
    business_headlines_list = list()
    india_Business_news_list = list()
    international_Business_news_list = list()
    ## for Business headlines
    for divTag1 in divTag:
        for divTag2 in divTag1.find_all("div", {"id": "c_wdt_list_2"}):
            for ulTag in divTag2.find_all("ul", {"class": "cvs_wdt clearfix"}):
                for span in ulTag.find_all("span", {"class": "w_tle"}):
                    for a in span.find_all('a', href=True):
                        # print(a.string)
                        business_headlines_list.append(a.string)

    ## for india Business news & international
    for divTag1a in divTag:
        for divTag2 in divTag1a.find_all("div", {"id": "c_listing_wdt_1"}):
            i = 1
            j = 1
            for divTag3 in divTag2.find_all("div", {"class": "top-newslist small"}):
                for ulTag in divTag3.find_all("ul", {"class": "clearfix"}):
                    for liTag in ulTag:
                        for span in liTag.find_all("span", {"class": "w_tle"}):
                            for a in span.find_all('a', href=True):
                                # print(a.string)
                                if i == 1:
                                    india_Business_news_list.append(a.string)
                                elif i == 2:
                                    international_Business_news_list.append(a.string)
                    i += 1
            for divTag3a in divTag2.find_all("div", {"class": "headlines-list"}):
                for divTag3a1 in divTag3a.find_all("div", {"class": "news_card"}):
                    for ulTag in divTag3a1.find_all("ul", {"class": "clearfix"}):
                        for liTag in ulTag:
                            for span in liTag.find_all("span", {"class": "w_tle"}):
                                for a in span.find_all('a', href=True):
                                    # print(a.string)
                                    if j == 1:
                                        india_Business_news_list.append(a.string)
                                    elif j == 2:
                                        international_Business_news_list.append(a.string)
                    j += 1

    return business_headlines_list,india_Business_news_list,international_Business_news_list

a,b,c = Business_news(word)

hdrs = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://cssspritegenerator.com',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
nse_stock_url ='https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json'
#nse_stock_url = 'http://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json'
url_response = requests.get(nse_stock_url)
print("url_response = " ,url_response)
open_nse_url = urllib2.Request(url=nse_stock_url,headers=hdrs)
opener = urllib2.build_opener()
f = opener.open(open_nse_url)
stock_json_data = dict()
stock_json_data = json.loads(f.read()).decode()
#print(a,'\n',b,'\n',c)
print('*'*60)
print(stock_json_data)







