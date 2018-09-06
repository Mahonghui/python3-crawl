# crawl all mentors in cse of seu
# incluing: research point, name, cv_href

# -*- coding: utf-8 -*-

import requests
from lxml import etree
from traceback import print_exc
import json

class CrawlMentorInfo():

	def __init__(self, url):

		self.url = url
		self.base_url = 'cse.seu.edu.cn'
		self.file_path = '/Users/mahonghui/Desktop/PythonCrawl/'
		self.file_name = 'MentorInfo.json'

		self.InfoDict = {}

	def getHTML(self):
		try:
			header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15}'}
			response = requests.get(self.url, headers=header)
			response.raise_for_status()
			response.encoding = response.apparent_encoding
			return response.text
		except Exception:
			return ''
			print_exc()

	def parseInfo(self):

		html = self.getHTML()
		if html != '':
			selector = etree.HTML(html)
			divs = selector.xpath('//div[@class="content"]/div')
			for div in divs:
				ulist = []
				
				direction = div.xpath('./h2/text()')[0]

				if direction == ' ':
					continue

				infos = div.xpath('./table/tr/td')
				for teacher in infos:
					item = {}
					name = teacher.xpath('./a/text()')[0]
					linkage = self.base_url + teacher.xpath('./a/@href')[0]
					item['name'] = name
					item['linkage'] = linkage
					ulist.append(item)

				self.InfoDict[direction] = ulist

		else:
			print_exc()





	def to_json(self):
		# json.dump(self.InfoDict, open(self.file_path + self.file_name, 'a'), ensure_ascii=False, indent=4)

		# prettfy json
		json_text = json.dumps(self.InfoDict, ensure_ascii=False, indent=4)
		formated_json = '\n'.join([line.rstrip() for line in json_text.splitlines()])
		with open(self.file_path + self.file_name, 'w') as f:
			f.write(formated_json)
			f.close()		





obj = CrawlMentorInfo('http://cse.seu.edu.cn/CSE/UI/Teacher/TeacherDirection.aspx')
obj.getHTML()
obj.parseInfo()
obj.to_json()



