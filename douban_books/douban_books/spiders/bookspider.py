# coding: utf-8
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request

from douban_books.items import DoubanBooksItem


class CrawlNewBooks(CrawlSpider):

    name = 'doubanbooks'
    start_urls = ['https://book.douban.com/latest?icn=index-latestbook-all']

    def parse(self, response):
        selector = Selector(response)
        fic_books = selector.xpath('//*[@id="content"]/div/div[2]/ul/li')
        nonfic_books = selector.xpath('//*[@id="content"]/div/div[3]/ul/li')

        for book in (fic_books + nonfic_books):
            item = DoubanBooksItem()
            item['name'] = book.xpath('./div/h2/a/text()').extract()[0]
            score = book.xpath('./div/p[1]/span[2]/text()').extract()[0]

            # some scores are characters or null
            try:
                rank = float(score)
            except ValueError:
                rank = 0
            item['rank'] = rank

            author = book.xpath('./div/p[2]/text()').extract()[0].split('/')[0].strip()
            item['author'] = author

            intro = book.xpath('./div/p[3]/text()').extract()[0].strip()
            item['intro'] = intro

            cover_url = book.xpath('./a/img/@src').extract()[0]
            item['cover_url'] = cover_url

            yield item
