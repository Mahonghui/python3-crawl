from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time

# name = '黄山'
# dest = '中国'
# driver = Chrome(executable_path='./chromedriver')
# driver.start_client()
# driver.get('https://www.tripadvisor.cn/')

# mag_span = driver.find_element_by_xpath('//*[@id="taplc_masthead_search_0"]/div/span[1]')
# mag_span.click()
# time.sleep(2)

# name_input = driver.find_element_by_xpath('//*[@id="mainSearch"]')
# address_input = driver.find_element_by_xpath('//*[@id="GEO_SCOPED_SEARCH_INPUT"]')
# search_btn = driver.find_element_by_xpath('//*[@id="SEARCH_BUTTON"]')
# name_input.send_keys(name)
# address_input.send_keys(dest)
# search_btn.click()
# time.sleep(3)

def get_url_by_short(venue_name, venue_address):
	driver = Chrome(executable_path='./chromedriver')
	driver.start_client()
	driver.get('https://www.tripadvisor.cn')
	time.sleep(2)
	# venue_name
	search_btn = driver.find_element_by_xpath('//*[@id="taplc_masthead_search_0"]/div/span[1]')
	search_btn.click()
	time.sleep(3)
	print(driver.page_source)
	driver.find_element_by_id('mainSearch').send_keys(venue_name)
	driver.find_element_by_id('GEO_SCOPED_SEARCH_INPUT').send_keys(venue_address)
	time.sleep(2)
	click_btn = driver.find_element_by_xpath('//*[@id="SEARCH_BUTTON"]')
	print(click_btn)
	click_btn.click()
	time.sleep(3)
	return driver.current_url

get_url_by_short('黄山', '中国')