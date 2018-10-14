

import requests, json, csv, time, os
from io import StringIO
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

#先拿到全部幣種的連結
url = "https://s2.coinmarketcap.com/generated/search/quick_search.json"
res = json.loads(requests.get(url).text)
TokenLink_list = []
for k in res:
    TokenLink_list.append("https://coinmarketcap.com/currencies/"+k["slug"])
###


print("目前CMC上有"+str(len(TokenLink_list))+"種幣別")

lens = len(TokenLink_list)-1
for i in TokenLink_list:
    try:
        url = i+"/#markets"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        res = BeautifulSoup(r.text, "lxml")

        #token name / token link / rank / coin type
        token_name = res.find("h1", {"class":"details-panel-item--name"}).text.split("\n")[2]
        token_link = i
        rank = res.find("ul", {"class":"list-unstyled details-panel-item--links"}).text.split("\n")[2].lstrip(" Rank")
        coin_type = res.find("ul", {"class":"list-unstyled details-panel-item--links"}).text.split("\n")[-3]
        ###
        
        #average volume
        url = i+"/historical-data/"
        r = requests.get(url, headers=headers)
        html_df = pd.DataFrame(pd.read_html(StringIO(r.text))[0])
        avg_volume = pd.to_numeric(html_df["Volume"], ).sum()/30
        ###
        
        #在幾個交易所上架？（listing_exchange） / 主要交易所（main_exchange） / 在主要交易所的交易比例（percent_biggest）
        url = i+"/#markets"
        r = requests.get(url, headers=headers)
        html_df = pd.DataFrame(pd.read_html(StringIO(r.text))[0])
        html_df["Volume (24h)"] = html_df["Volume (24h)"].str.extract('(\d+)', expand=True).astype(int)
        html_df["Volume (%)"] = html_df["Volume (%)"].str.rstrip("%").astype(float)

        percent_biggest = 0
        for i in html_df["Source"].unique():
            freq = 0
            percent = 0
            for ii in range(0, len(html_df["Source"])):
                if i == html_df["Source"][ii]:
                    percent+=html_df["Volume (%)"][ii]
                    freq+=1 
                if i == 0:
                    percent_biggest = percent
                if percent > percent_biggest:
                    percent_biggest = percent
                    main_exchange =  html_df["Source"][ii]
        listing_exchange = len(html_df["Source"].unique())
        ###
        
        final_list = [token_name, token_link, avg_volume, listing_exchange, main_exchange, percent_biggest, rank, coin_type]
        
        date = time.strftime("%Y%m%d", time.localtime())
        
        with open(os.path.expanduser("~/Desktop/COBINHOOD/RuralEncircleCity{}.csv".format(date)), "a") as csvfile:
            Writer = csv.writer(csvfile, delimiter=",")
            Writer.writerow(final_list)
        
        print("已抓下{}，".format(token_name)+"還剩"+str(lens)+"種幣別需抓下")
        lens-=1
    
    except Error as e:
        print(e)
        print("Error :{}".format(k["slug"]))





