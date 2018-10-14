
import requests, csv, re, time, random, os, urllib, datetime, codecs
from bs4 import BeautifulSoup
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import TelegramClient
from telethon.errors.rpc_error_list import (FloodWaitError, InviteHashInvalidError, InviteHashExpiredError)
from telethon.tl.types import InputPeerChannel

try:
	os.remove(os.path.expanduser("~/Desktop/COBINHOOD/trackico_telegram.csv"))
except FileNotFoundError:
	print("No such file or directory")

"""
#拿到連結清單
link_list = []
page = 1
while True:
	print(page)
	time.sleep(random.randint(0, 1))
	url = "https://www.trackico.io/closed/{}/".format(page)
	res = BeautifulSoup(requests.get(url, allow_redirects = False).text, "lxml")
	if res.text != "":
		list = res.findAll("a", {"class":"card-body text-center pt-1 pb-10"})
		for i in list:
			print("https://www.trackico.io"+i["href"])
			link_list.append(["https://www.trackico.io"+i["href"], i["href"].replace("/ico/", "").rstrip("/")])
		page = page+1
	else:
		print("final page: {}".format(page-1))
		break

#拿到telegram群組連結清單
info_list = []
for i in link_list:
	res = BeautifulSoup(requests.get(i[0]).text, "lxml")

	name = res.find("h1", {"class":"h2"}).text.split("\n")[0]
	try:
		telegram_link = res.find("a", {"class":"btn btn-square btn-telegram m-1 text-white"})["href"]
		telegram_name = telegram_link.split("/")[-1]
	except TypeError:
		telegram_link = "N/A"
		telegram_name = "N/A"

	print([name, telegram_link, telegram_name])
	info_list.append([name, telegram_link, telegram_name])

with open("/Users/harry/Desktop/COBINHOOD/trackico_telegram.csv", "w") as csvfile:
	Writer = csv.writer(csvfile, delimiter=",")
	for i in info_list:
		Writer.writerow(i)

info_list = []
with open("/Users/harry/Desktop/COBINHOOD/trackico_telegram.csv", "r", encoding="utf8") as csvfile:
	Reader = csv.reader(csvfile, delimiter = ",")
	for i in Reader:
		info_list.append(i)
print(info_list)
"""











#將名單輸入在這裡
info_list = [['3DToken', 'https://t.me/ico_3dtoken', 'ico_3dtoken', "01/01/2018"]]










#build connection
def connect_to_telegram(input_id, input_hash, input_phone):

	client = TelegramClient("Hank7", input_id, input_hash)
	
	client.connect()
	if not client.is_user_authorized():
		client.send_code_request(input_phone)
		try:
			client.sign_in(code=input('Enter code: '))
		except SessionPasswordNeededError:
			client.sign_in(password=getpass.getpass())
	print("connect success, ", client.get_me())

	return client

#parameter
error_list = []
num = 0
client = connect_to_telegram(195706, "4aee340fd75d3e892c572d2b8e5fd891", "+886911317165")

for i in range(0, len(info_list)):
	while True:
		if info_list[i][1] != "N/A":
			try:
				channel_query = client.get_input_entity(info_list[i][1])
				info_list[i].append(channel_query.channel_id)
				info_list[i].append(channel_query.access_hash)
				break
			except ValueError as e:
				print(e)
				error_list.append(info_list[i])
				break

			except FloodWaitError as e:
				print("wait...{}".format(e.seconds))
				time.sleep(e.seconds)

			except InviteHashInvalidError as e:
				print(e)
				error_list.append(info_list[i])
				break

			except InviteHashExpiredError as e:
				print(e)
				error_list.append(info_list[i])
				break

			except BrokenPipeError as e:
				print(e)
				time.sleep(30)
				break

			except AttributeError as e:
				print(e)
				time.sleep(30)
				break

			except RuntimeError as e:
				print(e)
				time.sleep(120)
		else:
			print(info_list[i][0], info_list[i][1])
			break



for i in info_list:

	
	date_list = i[3].split("/")
	#年/月/日
	offset_date = datetime.date(int(date_list[2]), int(date_list[0]), int(date_list[1]))
	message_list = [i[0], "N/A", "N/A", "N/A"]

	try:
		messages = GetHistoryRequest(
						peer=InputPeerChannel(i[-2], i[-1]),
						offset_date=offset_date, 
		                offset_id=0,
		                add_offset=0,
		                limit=1,
		                max_id=0,
		                min_id=0,
		                hash=0)
		start_id = client(messages).messages[0].id
		message_list[1] = start_id

		messages = GetHistoryRequest(
						peer=InputPeerChannel(i[-2], i[-1]),
						offset_date=offset_date + datetime.timedelta(days=30), 
		                offset_id=0,
		                add_offset=0,
		                limit=1,
		                max_id=0,
		                min_id=0,
		                hash=0)
		end_id = client(messages).messages[0].id
		message_list[2] = end_id
		
		messages = client.get_messages(
						entity=InputPeerChannel(i[-2], i[-1]),
		                offset_id=0,
		                add_offset=0,
		                limit=end_id-start_id+2,
		                max_id=end_id+1,
		                min_id=start_id)

		id_list = []
		for k in range(0, len(messages)):
			if messages[k].message is not None:
				id_list.append(messages[k].from_id)
		message_list[3] = len(set(id_list))
		
		print(message_list)

		with open(os.path.expanduser("~/Desktop/telegram message/telegram_message_count.csv"), "a", newline="") as csvfile:
			#message_list=[Token Sale開始時的訊息數, Token Sale過30天的訊息數, 不重複發言數]
			writer = csv.writer(csvfile)
			writer.writerow(message_list)

	except Exception as e:
		print(e, " ", i[0])
		error_list.append(i)
		continue

with open(os.path.expanduser("~/Desktop/telegram message/telegram_message_error.csv"), "w", newline="") as csvfile:
	writer = csv.writer(csvfile)
	for ele in error_list:
		writer.writerow(ele)






"""
ii = 0
while ii<= 5:
	try:
		client = TelegramClient('Hank', api_id, api_hash)
		client.start()
		messages = client.get_messages("altplanet_ico", limit=None, offset_date=datetime.date(2018, 6, 10), wait_time=0)
		
		print(messages)
		final_list = []
		for index in range(0, len(messages)):
			id = messages[index]
			message = messages[index].message
			date = messages[index].date
			list = [id, message, date] 
			final_list.append(list)
		with open("/Users/harry/Desktop/telegram message/message_24hr_{}.csv".format("altplanet_ico"), "w", newline="") as csvfile:
			writer = csv.writer(csvfile)
			if not final_list:
				break
			else:
				for i in final_list:
					writer.writerow(i)
		print("altplanet_ico", "end", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		time.sleep(2)
		break
	
	except RuntimeError:
		print("altplanet_ico", "rerun", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		time.sleep(5)
		ii += 1
	
	except:
		traceback.print_exc()
		ii += 1
"""



