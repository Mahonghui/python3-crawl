# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup as bs 

from pushover import PushIt


def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
	except:
		return ''
	else:
		return r.text


def parseWeather(Infolist, html):
	soup = bs(html, 'html.parser')
	lis = soup.find_all('li', class_=re.compile(r'^sky skyid'))
	try:
		for li in lis:
			day = li.find('h1').string.split('（')[0]
			wea = li.find('p', class_='wea').string
			temp = li.find('p', class_='tem')
			high_temp = temp.find('span')
			low_temp = temp.find('i').string
			if type(high_temp) == type(None):
					high_temp = ''
					tempture = low_temp
			else:
				high_temp = high_temp.string
				tempture = high_temp + '/' + low_temp

			Infolist.append([day, wea, tempture])
	except:
		traceback.print_exc()
		pass



def printInfo(Infolist):
	header = '{0:^5}\t{1:{3}^10}\t{2:^10}'
	print(header.format('日期', '天气', '温度', chr(12288)))
	for i in range(len(Infolist)):
		item = Infolist[i]
		print(header.format(item[0], item[1], item[2], chr(12288)))


def push_messages(Info_list):

	api_temp = 'https://api.pushover.net/1/messages.json?user={user}&token={token}&message={msg}'
	user = 'un7nwysd2ma32rvjpwzvmsbzck2iqv'
	token = 'aktaskhj8ygqgwd4tkwjsxwa6cgkyd'

	header = '{0:^5}\t{1:^5}\t{2:^5}'
	message = header.format('日期', '天气', '温度') + '\n'
	for weather in Info_list:
		message += header.format(weather[0], weather[1], weather[2]) + '\n'

	# push message to my device
	my_push = PushIt()
	my_push.push(message)

# 	full_api = api_temp.format(
# 			user= user,
# 			token= token,
# 			msg = message
# 		)
# 	return full_api

# push single message

# def push_message(message):
# 	r = requests.post(message)

def main():
	url = 'http://www.weather.com.cn/weather/101191301.shtml'
	Infolist = []

	html = getHTMLText(url)
	parseWeather(Infolist, html)
	# printInfo(Infolist)

	msg = push_messages(Infolist)
	# push_message(msg)



if __name__ == '__main__':
	main()
