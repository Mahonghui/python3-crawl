# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
from scrapy.conf import  settings
from pymongo import MongoClient

class Douban250Pipeline(object):

    def __init__(self):
        file = os.path.dirname(__file__) + '/douban250.json'
        self.file = open(file, 'wb')

    def process_item(self, item, spider):

        method = settings['EXPORT_METHOD']

        if method == 'mongodb':
            host = settings['MONGO_HOST']
            port = settings['MONGO_PORT']
            db_name = settings['MONGO_DB']
            doc_name = settings['MONGO_DOC']

            con = MongoClient(host, port)
            db = con[db_name]
            doc = db[doc_name]

            dic_item = dict(item)
            doc.insert(dic_item)


        ### 将数据导出json文件
        # json_text = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        # self.file.write(json_text)
        #
        # # also works
        # # json.dump(dict(item), self.file, ensure_ascii=False)
        return item



    def spider_closed(self, spider):
        self.file.close()
