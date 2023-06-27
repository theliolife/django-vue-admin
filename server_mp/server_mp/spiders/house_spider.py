# encoding:utf-8

import random
import time
import re
import scrapy
from datetime import datetime

# CREATE TABLE `sp_house` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `house_code` varchar(100) DEFAULT NULL,
#   `price` varchar(100) DEFAULT NULL,
#   `title` varchar(100) DEFAULT NULL,
#   `url` varchar(200) DEFAULT NULL,
#   `img` varchar(300) DEFAULT NULL,
#   `operate_time` date DEFAULT NULL,
#   `size` float DEFAULT NULL,
#   `ctime` datetime DEFAULT NULL,
#   `utime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

class NewsSpider(scrapy.Spider):
    name = 'house'

    # 允许此爬虫抓取的域的字符串的可选列表，指定一个列表可以抓取，其它就不会抓取了。
    allowed_domains = ['bj.zu.ke.com']

    # 当没有指定特定网址时，爬虫将开始抓取的网址列表。
    start_urls = ['https://bj.zu.ke.com/zufang/rs五棵松/']
    base_url = 'https://bj.zu.ke.com/zufang/pg{0}rs五棵松/#contentList'

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
        for result in response.xpath('//div[@class="content__list--item"]'):
            item = {}
            item['house_code'] = result.xpath('@data-house_code').get()

            item['price'] = result.xpath(
                './/div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()').extract_first()

            item['title'] = result.xpath('.//p[@class="content__list--item--title"]/a/text()')[0].extract()
            item['title'] = self.get_chinese_str(item['title'])
            item['url'] = 'https://bj.zu.ke.com' + result.xpath('.//a[@class="content__list--item--aside"]/@href').get()
            item['img'] = result.xpath('.//a[@class="content__list--item--aside"]/img/@src').get()

            if type(item['url']) == str:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }

                # 请求详情页
                yield scrapy.Request(
                    url=item['url'],
                    callback=self.parse_detail,
                    headers=headers,
                    meta={"item": item}
                )

            yield item

        # 计算下一页的 URL
        # self.page_num += 1
        # next_url = self.base_url.format(self.page_num)
        #
        # print("===================")
        # print(next_url)
        # # 如果下一页的 URL 不是最后一页，则继续请求下一页
        # if next_url:
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        #     }
        #     sec = random.uniform(1, 3)
        #     time.sleep(sec)
        #     yield scrapy.Request(url=next_url, headers=headers, callback=self.parse)

    # 解析详情页
    def parse_detail(self, response):
        item = response.meta["item"]
        # 维护时间
        item["operate_time"] = response.xpath("//div[@class='content__subtitle']/text()").extract_first()
        item["operate_time"] = self.get_number_str(item['operate_time'])
        item["size"] = response.xpath("//div[@class='content__article__info']/ul/li[position()=2]/text()").extract_first()
        item["size"] = self.get_number_str(item['size'])
        now = datetime.now()
        item["ctime"] = now.strftime("%Y-%m-%d %H:%M:%S")
        yield item  # 对返回的数据进行处理



    # def user_agent(self):
    #     # 读取 user_agents.txt 文件
    #     with open(self.settings.get('USER_AGENT_LIST')) as f:
    #         user_agents = f.read().splitlines()
    #
    #     # 随机选择一个 User-Agent
    #     user_agent = random.choice(user_agents)
    #
    #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #     print(user_agent)
    #     return user_agent

    def get_chinese_str(self, astr):
        res = re.findall('[\u4e00-\u9fa5|0-9]', astr)

        str_return = ''
        for one in res:
            str_return = str_return + one

        return str_return

    def get_number_str(self, astr):
        res = re.findall('[0-9|-|.]', astr)

        str_return = ''
        for one in res:
            str_return = str_return + one

        return str_return