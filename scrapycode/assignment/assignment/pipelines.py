# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo.mongo_client import MongoClient
import csv


class AssignmentPipeline(object):

    db_name = 'jd'
    collection_name = 'meidi'

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client[self.db_name]

        file = './comments.csv'
        self.fp = open(file, 'w+')
        headers = ['creationTime', 'user', 'referenceName', 'content']
        self.csv_file = csv.DictWriter(self.fp, headers, extrasaction='ignore')
        self.csv_file.writeheader()

    def process_item(self, item, spider):
        item_dict = dict(item)

        self.db[self.collection_name].insert_one(item_dict)
        self.csv_file.writerow(item_dict)
        return item

    def close_spider(self, spider):
        self.client.close()
        self.fp.close()