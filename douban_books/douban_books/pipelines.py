# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings
import requests
import os

class DoubanBooksPipeline(object):


    def __init__(self):

        db_host = settings['MONGO_HOST']
        db_name = settings['MONGO_DB']
        doc_name = settings['MONGO_DOC']

        conn = MongoClient(host=db_host)
        my_db = conn[db_name]
        self.my_doc = my_db[doc_name]

        self.img_dir = settings['IMG_DIR']

        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)
        else:
            os.chdir(self.img_dir)
            os.system('rm ./*')

    def process_item(self, item, spider):
        book_name = item['name']
        file_name = self.img_dir + item['cover_url'].split('/')[-1]

        header = {'User-Agent': settings['User-Agent']}
        r = requests.get(item['cover_url'], headers = header)

        with open(file_name, 'wb') as f:
            f.write(r.content)
            f.close()

        item['cover_location'] = file_name
        self.my_doc.insert(dict(item))
        return item

