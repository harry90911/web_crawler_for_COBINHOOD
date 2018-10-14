

import requests, csv, re, time, random, os
from bs4 import BeautifulSoup


try:
	os.remove(os.path.expanduser("~/Desktop/COBINHOOD/trackico_info.csv"))
except FileNotFoundError:
	print("No such file or directory")

link_list = []
page = 1
while True:
	print(page)

	#可以將closed改為ongoing
	url = "https://www.trackico.io/closed/{}/".format(page)
	res = BeautifulSoup(requests.get(url, allow_redirects = False).text, "lxml")
	if res.text != "":
		list = res.findAll("a", {"class":"card-body text-center pt-1 pb-10"})
		for i in list:
			link_list.append(["https://www.trackico.io"+i["href"], i["href"].replace("/ico/", "").rstrip("/")])
		page+=1
	else:
		print("final page: {}".format(page-1)+"，共"+str(len(link_list))+"個案子")
		break

with open(os.path.expanduser("~/Desktop/COBINHOOD/trackico_icolink.csv"), "w", newline = "") as csvfile:
	Writer = csv.writer(csvfile, delimiter = ",", quoting = csv.QUOTE_NONE)
	for i in link_list:
		Writer.writerow(i)

lens = len(link_list)-1
for link in link_list:

	final_list = []

	res = BeautifulSoup(requests.get(link[0]).text, "lxml")
	
	#案子名稱
	name = res.find("h1", {"class":"h2"}).text.split("\n")[0]
	final_list.append(name)

	#類別
	category = res.find("div", {"class":"card-body p-3"}).text.split("\n")[9]
	final_list.append(category)

	list = res.find("div", {"class":"col-md-4 col-xl-3 d-none d-md-block"})

	#解析表格
	middle_list = []
	for i in list.text.split("\n"):
		if i != "":
			middle_list.append(i)
	
	#地區
	try:
		if middle_list[middle_list.index('Country')+1] is not None:
			country = middle_list[middle_list.index('Country')+1]
	except:
		country = "N/A"

	#telegram連結
	try:
		if res.find("a", {"class":"btn btn-square btn-telegram m-1 text-white"})["href"] is not None:
			telegram_link = res.find("a", {"class":"btn btn-square btn-telegram m-1 text-white"})["href"]
	except:
		telegram_link = "N/A"
	
	#Pre-Sale
	try:
		if middle_list[middle_list.index("Pre-Sale")] is not None:
			presale_start = middle_list[middle_list.index('Pre-Sale')+1][0:10]
			presale_end = middle_list[middle_list.index('Pre-Sale')+2].strip("- ")[0:10]
	except:
		presale_start = "N/A"
		presale_end = "N/A"

	#Token Sale
	try:
		if middle_list[middle_list.index("Token Sale")] is not None:
			tokensale_start = middle_list[middle_list.index('Token Sale')+1][0:10]
			tokensale_end = middle_list[middle_list.index('Token Sale')+2].strip("- ")[0:10]
	except:
		tokensale_start = "N/A"
		tokensale_end = "N/A"

	#Platform
	try:
		if middle_list[middle_list.index("Platform")] is not None:
			platform = middle_list[middle_list.index('Platform')+1]
	except:
		platform = "N/A"
	
	#Alexa rank
	try:
		if middle_list[middle_list.index('Alexa rank')] is not None:
			alexa_rank = middle_list[middle_list.index('Alexa rank')+1].replace(",", "")
	except:
		alexa_rank = "N/A"

	#telegram參與人數
	try:
		if middle_list[middle_list.index('Telegram participants')] is not None:
			telegram_participants = middle_list[middle_list.index('Telegram participants')+1].replace(",", "")
	except:
		telegram_participants = "N/A"

	#twitter追蹤者
	try:	
		if middle_list[middle_list.index('Twitter followers')] is not None:
			twitter_followers = middle_list[middle_list.index('Twitter followers')+1].replace(",", "")
	except:
		twitter_followers = "N/A"

	#youtube video views
	try:
		if middle_list[middle_list.index('Promotional video views')] is not None:
			video_views = middle_list[middle_list.index('Promotional video views')+1].replace(",", "")
	except:
		video_views = "N/A"

	#到另外一個連結找資訊
	res = BeautifulSoup(requests.get(link[0]+"#financial").text, "lxml")
	list = res.find("div", {"class":"col-md-6"})
	middle_list = []
	for i in list.text.split("\n"):
		if i != "":
			middle_list.append(i)
	
	#Token Price
	try:
		if middle_list[middle_list.index('Token Price')] is not None:
			token_price = middle_list[middle_list.index('Token Price')+1].replace(",", "")
	except:
		token_price = "N/A"

	#Token for sale
	try:
		if middle_list[middle_list.index('Token for sale')] is not None:
			token_for_sale = middle_list[middle_list.index('Token for sale')+1].replace(",", "")
	except:
		token_for_sale = "N/A"

	#Token supply
	try:
		if middle_list[middle_list.index('Token supply')] is not None:
			token_supply = middle_list[middle_list.index('Token supply')+1].replace(",", "")
	except:
		token_supply = "N/A"

	#Total raised
	try:
		if middle_list[middle_list.index("Total raised")] is not None:
			total_raised = middle_list[middle_list.index('Total raised')+1]
	except:
		total_raised = "N/A"

	final_list = [
		name,
		category,
		country,
		telegram_link,	
		presale_start,
		presale_end,
		tokensale_start,
		tokensale_end,
		platform,	
		alexa_rank,
		telegram_participants,
		twitter_followers,
		video_views,
		token_price,
		token_for_sale,
		token_supply,
		total_raised]

	print(final_list)
	with open(os.path.expanduser("~/Desktop/COBINHOOD/trackico_info.csv"), "a", newline="") as csvfile:
		Writer = csv.writer(csvfile, delimiter=",")
		try:
			Writer.writerow(final_list)
		except UnicodeEncodeError:
			print("wtf")
	
	print("已抓下{}，".format(name)+"還剩"+str(lens)+"個ICO需抓下")
	lens-=1


