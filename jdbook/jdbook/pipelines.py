# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings

class JdbookPipeline(object):
    def process_item(self, item, spider):
        conn = MongoClient(settings['MONGO_HOST'])
        my_collec = conn[settings['MONGO_DB']][settings['MONGO_COL']]

        my_collec.insert(dict(item))
        return item

