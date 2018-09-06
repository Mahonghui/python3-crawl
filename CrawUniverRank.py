# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
import bs4
import pygal

def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

def fillUnivList(ulist, html):
	if not html == "":
		soup = bs(html, 'html.parser')
		for tr in soup.find('tbody').children: # fetch children node
			if isinstance(tr, bs4.element.Tag): # exclude string node
				tds = tr('td')
				ulist.append([tds[0].string, tds[1].string, tds[3].string])
	


def printList(ulist, num):
	templete = "{0:^10}\t{1:{3}^10}\t{2:^10}"
	print(templete.format("排名", "高校", "得分", chr(12288)))
	for i in range(num):
		u = ulist[i]
		print(templete.format(u[0], u[1], u[2], chr(12288)))


def main():
	url = 'http://zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
	ulist = []

	html = getHTMLText(url)
	fillUnivList(ulist, html)
	# printList(ulist, 20)

	hist = pygal.Bar(x_label_rotation=45, show_legend=False)
	hist._title='University Rank'
	hist.x_labels=[e[1] for e in ulist][:15]

	hist.add('', [float(e[2]) for e in ulist][:15])
	hist.render_in_browser()






if __name__ == '__main__':
	main()