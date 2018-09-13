# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from szkj.items import SzkjItem
import re

class SzkjInfo(CrawlSpider):

    name = 'szkj'
    start_urls = ['http://www.szkj.gov.cn/kjzc']
    base_url = 'http://www.szkj.gov.cn'

    def parse(self, response):
        selector = Selector(response)
        open_lists = selector.xpath('//div[@class="left_public side2"]/div')
        for open_list in open_lists:
            url = open_list.xpath('./div/span/a/@href').extract()[0]
            yield Request(self.base_url + url, callback=self.parseArticle)

    def parseArticle(self, response):
        item = SzkjItem()
        selector = Selector(response)
        article_list = selector.xpath('//div[@class="open_list"]/ul/li')

        for article in article_list:
            arti_time = article.xpath('./div[2]/text()').extract()[0]
            year = arti_time.split('-')[0]

            if int(year) == 2017:
                item['date'] = arti_time
                arti_url = article.xpath('./div[1]/a/@href').extract()[0]

                yield Request(self.base_url + arti_url, callback=self.parseContent, meta={'item': item})


    def parseContent(self, response):
        item = response.meta['item']
        selector = Selector(response)

        title = selector.xpath('//div[@class="planed"]/h1/text()').extract()[0]
        item['title'] = title

        body = selector.xpath('//div[@class="txt"]')
        content = body.xpath('string(.)').extract()[0]
        item['content'] = content
        yield item


