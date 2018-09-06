# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs 
import re
import bs4
import traceback
import sys


def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return	r.text
	except:
		return ''


def extractStockInfo(slist, html):
	try:
		count = 0
		if html != '':
			soup = bs(html, 'html.parser')
			table = soup.find('table', class_='stockBlock')
			for tr in table.children:
				if isinstance(tr, bs4.element.Tag) and tr.find('a'):
					a = tr.find_all('a')
					stcok_name = a[1].string
					company_name = a[2].string

					href = a[1].attrs['href']
					market = href.split('/')[-3]
					code = href.split('/')[-2]
					stock_code = market + code

					slist.append([stock_code, stcok_name, company_name])
		else:
			print('Unable to fetch HTML content')
			sys.exit()

	except:
		traceback.print_exc()



def printSList(slist):
	header = '{0:<10}\t{1:^10}\t{2:{3}^10}'
	print(header.format('股票代码', '股票简称','公司名称', chr(12288)))
	for i in range(len(slist)):
		item = slist[i]
		print(header.format(item[0], item[1], item[2], chr(12288)))


def main():
	url = 'http://www.yz21.org/stock/info/'
	slist = []

	html = getHTMLText(url)
	extractStockInfo(slist, html)

	for i in range(2,6):
	 	html = getHTMLText(url + 'stocklist_' + str(i) + '.html')
	 	extractStockInfo(slist, html)

	printSList(slist)

	print('\n' + 'Total stock: '+ str(len(slist)))




main()