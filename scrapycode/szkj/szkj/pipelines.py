# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from pymongo import MongoClient
from scrapy.conf import settings

class SzkjPipeline(object):

    mongo_host = settings['MONGO_HOST']
    mongo_db = settings['MONGO_DB']
    mongo_doc = settings['MONGO_DOC']

    conn = MongoClient(host=mongo_host)
    my_db = conn[mongo_db]
    my_doc = my_db[mongo_doc]

    def process_item(self, item, spider):
        self.my_doc.insert(dict(item))
        return item