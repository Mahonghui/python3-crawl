# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from assignment.items import AssignmentItem
import json
import re
import time



class CommentsSpider(Spider):
    name = 'comments'
    # allowed_domains = ['www.search.jd.com']
        url_template = 'https://search.jd.com/Search?keyword={kw}&enc=utf-8&page={page}&s={start}'

    keyword = u'美的热水器'
    search_url = url_template.format(kw=keyword, page=1, start=1)
    start_urls = [search_url]

    def parse(self, response):
        url_template = 'https://search.jd.com/Search?keyword=美的热水器&enc=utf-8&page={page}&s={start}'
        com_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv46445&productId={sku_id}&sortType=5&score=0&page={page}&pageSize=10'

        body = Selector(response)
        sku_ids = body.xpath('//li[@class="gl-item"]/@data-sku').extract()
        print('*'*60)
        print(response.request.url)
        item = AssignmentItem()
        for sku in sku_ids:
            for page in range(1):
                url = com_url.format(sku_id=sku, page=page)
                yield Request(url, callback=self.parse_comment, meta={'item': item})
                time.sleep(1)
        page = response.meta.get('page', 1)
        start = response.meta.get('start', 1)
        incr = response.meta.get('incr', 59)
        total_page = response.meta.get('total_page', 0)
        total_page = total_page + 1
        new_incr = incr - 1
        new_page = page + 2
        new_start = start + new_incr
        next_url = url_template.format(page=new_page, start=new_start)
        if total_page < 2:
            yield Request(next_url, callback=self.parse, meta={'page': new_page,
                                                           'start': new_start,
                                                           'incr': new_incr,
                                                           'total_page': total_page})

    def parse_comment(self, response):
        if response.text:
            content = response.text
            if 'fetchJSON' in content:
                content = re.search(r'^fetch.*?\((.*)\);', content, re.S).group(1)
            dicts = json.loads(content)
            item = response.meta.get('item')
            print(response.request.url)
            for comment in dicts['comments']:
                item['creationTime'] = comment['creationTime']
                item['user'] = comment['nickname']
                item['referenceName'] = comment['referenceName']
                item['content'] = comment['content']
                yield item
            time.sleep(1)




