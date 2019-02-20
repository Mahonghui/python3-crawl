# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

import os
import time
import json

def start_driver():
	driver = Chrome(executable_path='./chromedriver')
	driver.start_client()
	return driver

def start_search(driver, keyword):
	search_key = driver.find_element_by_xpath('//input[@id="key"]')
	search_key.send_keys(keyword)
	search_key.send_keys(Keys.ENTER)

def get_good_url(driver):
		urls = []
		item_url = 'https://item.jd.com/'
		goods_li = driver.find_elements_by_xpath('//ul[@class="gl-warp clearfix"]/li')		
		for li in goods_li:
			sku = li.get_attribute("data-sku")
			urls.append(item_url + sku + '.html')
		return urls, driver.current_url

def get_next_page(driver):
	next_a = driver.find_elements_by_xpath('//a[@class="pn-next"]')
	if next_a:
		return next_a[0]
	else:
		return None

def get_comment(driver, comment_list):
	comment_divs = driver.find_elements_by_xpath('//div[@class="comment-item"]')
	for item in comment_divs:
		comm_p = item.find_elements_by_xpath('.//p[@class="comment-con"]')
		if comm_p:
			comm = comm_p[0].text
		else:
			comm = '暂无'
		print(comm)
		comment_list.append(comm + '\n')

def jump_to_next_comment_page(driver):
	next_page = driver.find_element_by_xpath('//*[@id="comment-0"]/div[13]/div/div/a[7]')
	next_page.click()

def save(comment_list, path):
	with open(path, 'w') as f:
		json.dump(comment_list, f, ensure_ascii=False)


if __name__ == '__main__':
	base_url = 'https://www.jd.com/'
	keyword = '美的热水器'
	driver = start_driver()

	driver.get(base_url)

	start_search(driver, keyword)
	comment_list = []
	time.sleep(1)
	
	next_page = 1 # just to be not None for launch
	for _ in range(18):
		goods_url, current_url = get_good_url(driver)

		for url in goods_url:
			try:
				driver.get(url)
				comment_icon = driver.find_element_by_xpath('//li[@data-anchor="#comment"]')
				comment_icon.click()
				time.sleep(2)
				
				get_comment(driver, comment_list)
			except Exception as e:
				continue
				
			print('*'*60)
		driver.get(current_url)

	print('Done')
	print('-'*50)
	print('共计' + str(len(comment_list))+ '条评论')
	print('Bye bye')
	time.sleep(1)
	driver.close()
	save(comment_list, './comments.json')