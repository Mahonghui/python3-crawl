# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from douban250.items import Douban250Item

class DoubanSpider(CrawlSpider):
    name = 'douban250'
    start_urls = ['https://movie.douban.com/top250']
    url = 'https://movie.douban.com/top250'

    def parse(self, response):
        Item  = Douban250Item()
        selector = Selector(response)
        items = selector.xpath('//div[@class="item"]/div[@class="info"]')
        for movie in items:
            title = movie.xpath('div[@class="hd"]/a/span/text()').extract()
            movie_info = movie.xpath('div[@class="bd"]/p[@class=""]/text()').extract()
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()


            if quote:
                quote_str = quote[0]
            else:
                quote_str = 'No quote'
            print('star: ', star)
            Item['title'] = ';'.join(title)
            Item['movie_info'] = movie_info[0]
            Item['star'] = round(float(star[0]), 1)
            Item['quote'] = quote_str

            yield Item

            next_link = selector.xpath('//span[@class="next"]/link/@href').extract()
            if next_link:
                # print(url+next_link)
                yield Request(self.url + next_link[0], callback=self.parse)

