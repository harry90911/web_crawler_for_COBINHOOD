


import csv, requests, datetime, re, random, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

name_list = []
page = 1
while True:
	print("page{}".format(page))

	#可以將closed改為ongoing
	url = "https://www.trackico.io/closed/{}/".format(page)
	res = BeautifulSoup(requests.get(url).text, "lxml")
	list = res.findAll("a", {"class":"card-body text-center pt-1 pb-10"})
	for i in list:
		name_list.append(re.sub("ico", "", i["href"].strip("/")))
	page+=1
print(name_list)

with open(os.path.expanduser("~/Desktop/COBINHOOD/trackico_iconame.csv"), "w", newline = "") as csvfile:
	Writer = csv.writer(csvfile, delimiter = ",", quoting = csv.QUOTE_NONE)
	for i in name_list:
		Writer.writerow([i])

error_list = []

#需要在此變更webdriver的位置
#請到此下載webdriver:https://chromedriver.storage.googleapis.com/index.html?path=2.41/
driver = webdriver.Chrome("/Users/harry/anaconda/selenium/webdriver/chromedriver")

for name in name_list:

	print(name)
	link = "https://www.trackico.io/ico"+name+"/#statistics"
	driver.get(link)
	
	try:
		element = WebDriverWait(driver, random.randint(0,40)).until(EC.presence_of_element_located((By.ID, "alexa-stats")))
	except Exception as e:
		print(e)
		error_list.append(link)

	sleep_time = random.randint(0,2)
	time.sleep(sleep_time)

	try:
		alexa_list = []
		innerHTML = driver.execute_script("return Highcharts.charts['0'].series[0].options.data")

		for i in innerHTML:
			alexa_list.append([str(datetime.datetime.utcfromtimestamp(i[0]/1000))[0:10], i[1]])
	except Exception:
		print("alexa error")
		error_list.append(link)
		if error_list[-1] != link:
			error_list.append(link)

	try:
		telegram_list = []
		innerHTML = driver.execute_script("return Highcharts.charts['1'].series[0].options.data")
		for i in innerHTML:
			telegram_list.append([str(datetime.datetime.utcfromtimestamp(i[0]/1000))[0:10], i[1]])
	except Exception:
		print("telegram error")
		if error_list[-1] != link:
			error_list.append(link)

	with open(os.path.expanduser("~/Desktop/COBINHOOD/trackico_timeseries/{}_alexa.csv").format(name), "w", newline = "") as csvfile:
		Writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_NONE)
		for i in alexa_list:
			Writer.writerow(i)

	with open(os.path.expanduser("~/Desktop/COBINHOOD/trackico_timeseries/{}_telegram.csv").format(name), "w", newline = "") as csvfile:
		Writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_NONE)
		for i in telegram_list:
			Writer.writerow(i)

	with open(os.path.expanduser("~/Desktop/COBINHOOD/trackico_timeseries/error_list.csv"), "a", newline = "") as csvfile:
		Writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_NONE)
		for i in error_list:
			Writer.writerow([i])

with open(os.path.expanduser("~/Desktop/COBINHOOD/trackico_timeseries/error_list.csv"), "w", newline = "") as csvfile:
	Writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_NONE)
	for i in error_list:
		Writer.writerow([i])


