# -*- coding -*- 

from wxpy import *
from pymongo import MongoClient
import time

def get_top10():  
	conn = MongoClient()
	my_doc = conn.douban.Movie

	top_10 = my_doc.find().limit(10)
	return top_10


def make_msg(cursor):
	template = ' <{title}>这部电影非常好看，豆瓣评分：{star}, 看过的人这么评价它: “{quote}”, 你也去看看吧! '
	return [ template.format(
				title= row['title'].split(';')[0],
				star= row['star'],
				quote= row['quote'],
			) for row in cursor]


def send_msg(msg_list, friends):
	bot = Bot(cache_path=True)

	for friend in friends:
		f = ensure_one(bot.friends().search(friend))
		# for msg in msg_list:
		# 	f.send('hi! '+ f.nick_name + msg)
		# 	time.sleep(2)	
		time.sleep(6)
	print('done')

friends = ['yimmy']
cursor = get_top10()
msg_list = make_msg(cursor)
send_msg(msg_list, friends)