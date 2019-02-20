# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import csv

def start_chorme():
	driver = webdriver.Chrome(executable_path='./chromedriver')
	driver.start_client()
	return driver


def login(base_url,driver):

	if not driver.get_cookies():
		driver.get(base_url)
		account_sel = '#form_email'
		pwd_sel = '#form_password'
		time.sleep(3)
		acc = driver.find_element_by_css_selector(account_sel)
		pwd = driver.find_element_by_css_selector(pwd_sel)

		acc.clear()
		acc.send_keys('18752782893')
		pwd.clear()
		pwd.send_keys('mhh15151132122')

		chk = driver.find_element_by_css_selector('#form_remember')
		chk.click()

		submit = driver.find_element_by_css_selector('#lzform > fieldset > div.item.item-submit > input')
		submit.click()

		cookies = driver.get_cookies()
		# driver.delete_all_cookies()
		for cookie in cookies:
			if cookie['domain'] in driver.current_url:
				driver.add_cookie(cookie)
		driver.refresh()

	else:
		driver.get(base_url)



def get_info(info_list, driver):
	cards_xpath = '//div[@class="stream-items"]/div'
	info_cards = driver.find_elements_by_xpath(cards_xpath)

	for card in info_cards:
		if card.find_elements_by_xpath('./span[@class="reshared_by"]'):
			continue
		user = card.find_elements_by_xpath('.//div[@class="text"]/a[@class="lnk-people"]')[0].text

		quote = card.find_elements_by_xpath('.//blockquote[@class="quote-clamp"]/p')
		if quote:
			quote_str = quote[0].text
		else:
			continue

		create_time = card.find_elements_by_xpath('.//span[@class="created_at"]')
		ct = create_time[0].get_attribute('title').split(' ')[0]
		
		like_count = card.find_elements_by_xpath('.//span[contains(@class, "like-count")]')
		if like_count:
			like_count = int(like_count[0].get_attribute('data-count'))
		else:
			like_count = 0
		
		info_list.append([user, quote_str, like_count, ct])


def get_next(driver):
	next_page = driver.find_element_by_xpath('//span[@class="next"]/a').get_attribute('href')
	return next_page

def save_csv(info_list):
	header = ['用户', '内容', '点赞数', '发布时间']
	sorted_list = sorted(info_list, key=lambda x: x[2], reverse=True)
	full_path = __file__.split('.')[0]	
	full_path += '.csv'
	if os.path.exists(full_path):
		os.system('rm ' + full_path)

	with open(full_path, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerows(sorted_list)

	print('Done')



def main():

	base_url = 'https://www.douban.com/'
	driver = start_chorme()

	info_list = []
	login(base_url,driver)
	time.sleep(5) # wait for verifying

	for j in range(3): # hard code:crawl 3 pages 
		get_info(info_list, driver)
		next_page = get_next(driver)
		driver.get(next_page)

	save_csv(info_list)
	time.sleep(7)

	driver.quit()


if __name__ == '__main__':
	main()
