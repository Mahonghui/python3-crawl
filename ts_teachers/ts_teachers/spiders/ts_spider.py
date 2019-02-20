# encoding: utf-8

from scrapy import Spider
from scrapy.selector import Selector
from traceback import print_exc
import json

class Ts_Spider(Spider):
    '''爬取清华计算机系教师信息'''

    name = "ts_spider"
    start_urls = ["http://www.cs.tsinghua.edu.cn/publish/cs/4797/index.html"]
    titles = ('正高', '副高', '中级', '实验技术人员')
    base_url = 'http://www.cs.tsinghua.edu.cn'

    def parse(self, response):
        selector = Selector(response)
        box = selector.xpath('//div[@class="box_detail"]')
        h1s = box.xpath("./h1")
        uls = box.xpath("./ul")
        # skip headline
        h1s.pop(0)
        info = dict()
        try:
            for i in range(len(uls)):

                depart = h1s[i].xpath(".//text()").extract()[0]
                lis = uls[i].xpath("./li")
                info.setdefault(depart, [])
                for j in range(len(lis)):
                    title = self.titles[j]
                    names = lis[j].xpath(".//a/text()").extract()
                    hrefs = lis[j].xpath('.//a/@href').extract()
                    if names is not None and all([names, hrefs]):
                        info[depart].append([(name, title, self.base_url + href) for name, href in zip(names, hrefs) \
                                             if href is not None])
        except:
            print_exc()
        json_text = json.dumps(info, ensure_ascii=False, indent=4)
        formatted_json = '\n'.join([line.strip() for line in json_text.splitlines()])
        with open('output.json', 'w') as fp:
            fp.write(formatted_json)

