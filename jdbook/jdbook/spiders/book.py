# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
import json
import time


class BookSpider(RedisSpider):
    name = 'book'
    allowed_domains = ['jd.com', 'p.3.cn']

    redis_key = 'jd'
 #   start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')

        for dt in dt_list:
            item = {}

            item['b_cate'] = dt.xpath('./a/text()').extract_first()

            em_list = dt.xpath('./following-sibling::dd[1]/em')

            for em in em_list:
                item['s_href'] = em.xpath('./a/@href').extract_first()
                item['s_cate'] = em.xpath('./a/text()').extract_first()

                if item['s_href'] is not None:
                    yield scrapy.Request('https:'+item['s_href'],
                                         callback = self.parseBook,
                                         meta= {'item': deepcopy(item)})


    def parseBook(self, response):

        item = response.meta['item']
        li_list = response.xpath('//*[@id="plist"]/ul/li')
        base_url = 'https://list.jd.com'

        for li in li_list:
            item['book_img'] = li.xpath('.//div[@class="p-img"]//img/@src').extract_first()
            if item['book_img'] is None:
                item['book_img'] = li.xpath('.//div[@class="p-img"]//img/@data-lazy-img').extract_first()

            item['book_name'] = li.xpath('.//div[@class="p-name"]//em/text()').extract_first().strip()
            item['book_author'] = '/'.join(li.xpath('.//span[@class="p-bi-name"]/span/a/text()').extract())
            item['book_pub'] = li.xpath('.//span[@class="p-bi-store"]/a/@title').extract_first()
            item['pub_date'] = li.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()

            sku = li.xpath('./div/@data-sku').extract_first()
            price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(sku)

            yield scrapy.Request(price_url, callback=self.parsePrice, meta={'item': item})

        next_page = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(base_url + next_page,
                                 callback=self.parseBook,
                                 meta={'item': item}
                                 )

    def parsePrice(self, response):
        item = response.meta['item']
        json_dic = json.loads(response.text)

        if isinstance(json_dic, list):
            item['book_price'] = json_dic[0].get('op', 0)
        else:
            item['book_price'] = 0

        yield item
