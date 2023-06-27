# encoding:utf-8

import random
import time

import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'

    # 允许此爬虫抓取的域的字符串的可选列表，指定一个列表可以抓取，其它就不会抓取了。
    allowed_domains = ['news.qingdaonews.com']

    # 当没有指定特定网址时，爬虫将开始抓取的网址列表。
    start_urls = ['https://news.qingdaonews.com/qingdao/']
    base_url = 'https://news.qingdaonews.com/qingdao/node_91770_{0}.htm'

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }

    def __init__(self, *args, **kwargs):
        self.page_num = 1

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        for result in response.xpath('//div[@class="news_row clearfix"]'):
            title = result.xpath('string(.//h3)').get().strip()
            print("---------------------")
            print(title)
            yield {"title": title}

        # 计算下一页的 URL
        self.page_num += 1
        next_url = self.base_url.format(self.page_num)

        print("===================")
        print(next_url)
        # 如果下一页的 URL 不是最后一页，则继续请求下一页
        if next_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            sec = random.uniform(1, 3)
            time.sleep(sec)
            yield scrapy.Request(url=next_url, headers=headers, callback=self.parse)