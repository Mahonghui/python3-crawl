# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup as bs
import os
import traceback
import sys


def getHTML(url):

	header = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
		'Cookie': 'JSESSIONID=0231CB8A73F52C86DF8EA7819C7CAB28',
		'Connection': 'keep-alive',
	}
	try:
		r = requests.get(url, headers = header)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r
	except:
		traceback.print_exc()



def paseImage(ilist, html):
	if type(html) != type(None):

		soup = bs(html.text, 'html.parser')
		img_list = soup.find_all('image')

		for img in img_list:
			img_url = img.attrs['src']
			ilist.append(img_url)
	else:
		print('Fail to crawl')
		sys.exit(0)


def storeImage(url,ilist, dire):
	count = 0
	for i in range(len(ilist)):
		try:
			name = ilist[i].split('/')[-1]
			path = dire + name
			r = getHTML(url + ilist[i].strip())
			if not os.path.exists(dire):
				os.mkdir(dire)
			with open(path, 'wb') as f:
				f.write(r.content)
				count += 1
		except:
			traceback.print_exc()
			continue
			
		print('images fetched: ' + str(count) + '/' + str(len(ilist)))

def main():
	if len(sys.argv) == 1:
		url = 'http://www.seu.edu.cn'
	else:
		url = sys.argv[1]

	folder_name = re.search(r'www\.(.*)\.', url).group(1)

	ilist = []
	dire = '/Users/mahonghui/Desktop/PythonCrawl/images/' + folder_name + '/'

	html = getHTML(url)
	paseImage(ilist, html)
	storeImage(url,ilist, dire)

main()