# coding:utf-8

import requests
import re


def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ''



def parsePage(glist, html):
	try:
		plt = re.findall(r'"price":"\d*"', html)
		tlt = re.findall(r'"title":"(.*?)"', html)
		print(html)
		for i in range(len(plt)):
			price = eval(plt[i].split(':')[1])
			title = eval(tlt[i].split(':')[1])
			glist.append([title, price])
	except:
		print("Error")



def printGoodList(glist):
	header = '{0:^4}\t{1:{3}^10}\t{2:6}'
	print(header.format('编号', '商品名称', '价格', chr(12288)))

	for i in range(len(glist)):
		item = glist[i]
		print(header.format(i+1, item[0], item[1], chr(12288)))



def main():
	goods = 'macbook+pro'
	start_url = 'https://s.taobao.com/search?q=' + goods
	depth = 2
	glist = []

	for i in range(depth):
		try:
			
			url = start_url + str(i*48)
			html = getHTMLText(url)
			parsePage(glist, html)
			printGoodList(glist)
		except:
			print('Exception generated')

main()

