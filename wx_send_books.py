# -*- coding:utf-8 -*- 

from wxpy import *
from pymongo import MongoClient
import time

def get_topN(n):  
	conn = MongoClient()
	my_doc = conn.douban.new_book

	top_N = my_doc.find().limit(n)
	return list(top_N)


def make_msg(cursor):
	template = ' [豆瓣新书推荐]<{title}> /作者： {author}，豆瓣评分：{rank}。 简介: “{intro}”, 要不要了解一下~^?^ '
	return [ template.format(
				title= row['name'],
				author = row['author'],
				rank = str(row['rank']) if row['rank'] !=0 else '评分人数不足',
				intro= row['intro'],
			) for row in cursor], [ row['cover_location'] for row in cursor ]


def send_msg(msg_list, img_list, friends):
	bot = Bot(cache_path=True)

	for friend in friends:
		f = ensure_one(bot.friends().search(friend))
		for i in range(len(msg_list)):
			f.send('hi! '+ f.nick_name + msg_list[i])
			time.sleep(0.5)
			f.send_image(img_list[i])
			time.sleep(3)	
		time.sleep(6)
	print('done')

friends = ['yimmy', u'烙铁']
cursor = get_topN(5)
msg_list, img_list = make_msg(cursor)
send_msg(msg_list, img_list, friends)