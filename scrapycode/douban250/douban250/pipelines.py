# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os



class Douban250Pipeline(object):

    def __init__(self):
        file = os.path.dirname(__file__) + '/douban250.json'
        self.file = open(file, 'wb')

    def process_item(self, item, spider):

        json_text = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(json_text)

        # also works
        # json.dump(dict(item), self.file, ensure_ascii=False)
        return item

    def spider_closed(self, spider):
        self.file.close()
