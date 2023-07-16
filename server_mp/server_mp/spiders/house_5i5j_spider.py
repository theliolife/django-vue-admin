# coding=utf-8

import random
import time
import re
import os
import math
import json
import requests
import scrapy
from datetime import datetime
from geopy.distance import geodesic

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

def bdToGaoDe(lon, lat):
    """
    百度坐标转高德坐标
    :param lon:
    :param lat:
    :return:
    """

    PI = 3.14159265358979324 * 3000.0 / 180.0
    x = lon - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PI)
    lon = z * math.cos(theta)
    lat = z * math.sin(theta)
    return lon, lat


# https://lbs.amap.com/api/webservice/guide/api/direction
def walks(origin, destination):
    key = os.environ.get('GAO_DE_KEY')  ##输入自己key
    parameters = {'key': key, 'origin': origin, 'destination': destination}
    ##参数的输入，可以按照自己的需求选择出行时间最短，出行距离最短，不走高速等方案，结合自己需求设置，参考手册
    response = requests.get('https://restapi.amap.com/v3/direction/walking?parameters', params=parameters)
    text = json.loads(response.text)
    duration = text['route']['paths'][0]['duration']  ##出行时间
    ## 可以自己打印text看一下，能提取很多参数，出行时间、出行费用、出行花费等看自己需求提取

    return response.text

class NewsSpider(scrapy.Spider):
    name = 'house_5i5j'

    # 允许此爬虫抓取的域的字符串的可选列表，指定一个列表可以抓取，其它就不会抓取了。
    allowed_domains = ['bj.5i5j.com']

    # 当没有指定特定网址时，爬虫将开始抓取的网址列表。
    start_urls = ['http://bj.5i5j.com/zufang/o8n1/_五棵松']
    base_url = 'http://bj.5i5j.com/zufang/o8nn{0}/_五棵松'

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
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for result in response.xpath('//ul[@class="pList rentList"]/li'):
            item = {}
            item['source'] = '5i5j'

            imgInfoResult = result.xpath('.//div[@class="listImg"]/a/img/@src').extract_first()
            if imgInfoResult == None:
                imgInfoResult = ''
            item['img'] = imgInfoResult

            textInfoResult = result.xpath('.//div[@class="listCon"]')
            base_json = textInfoResult.xpath('.//h3/a').extract_first()
            pattern = 'houseid_var":"(.*?)"'
            item['house_code'] = re.findall(pattern, base_json)[0]

            operateTimeStr = textInfoResult.xpath('.//div[@class="listX"]/p[position()=3]/text()').extract_first()
            if operateTimeStr.encode('utf-8').find('今天发布') != -1:
                # 维护时间
                now = datetime.now()
                item["operate_time"] = now.strftime("%Y%m%d")
            else:
                pattern = '[1-2][0-9][0-9][0-9]-[0-1]{0,1}[0-9]-[0-3]{0,1}[0-9]'
                item['operate_time'] = re.findall(pattern, base_json)[0]

            item['price'] = textInfoResult.xpath(
                './/div[@class="listX"]/div[@class="jia"]/p[@class="redC"]/strong/text()').extract_first()

            item['title'] = textInfoResult.xpath('.//h3/a/text()').extract_first()

            item['url'] = 'https://bj.5i5j.com' + textInfoResult.xpath('.//h3/a/@href').extract_first()
            if item['url']:
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
        self.page_num += 1
        if self.page_num > 8:
            print('执行完毕')
            exit(1)
        next_url = self.base_url.format(self.page_num)
        # 如果下一页的 URL 不是最后一页，则继续请求下一页
        if next_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            sec = random.uniform(1, 3)
            time.sleep(sec)
            yield scrapy.Request(url=next_url, headers=headers, callback=self.parse)

    # 解析详情页
    def parse_detail(self, response):
        item = response.meta["item"]

        latText = response.xpath('//script[@type="text/javascript"]/text()').extract()[2]

        detailText = response.xpath('//div[@class="content fr"]')

        pattern = 'community_x = "(.*)";'
        longitude = re.findall(pattern, latText)
        if len(longitude) > 0:
            longitude = longitude[0]

        pattern = 'community_y = "(.*)";'
        latitude = re.findall(pattern, latText)
        if len(latitude) > 0:
            latitude = latitude[0]

        # 维护时间
        now = datetime.now()

        # item["longitude"] = longitude
        # item["latitude"] = latitude

        item["longitude"], item["latitude"] = bdToGaoDe(float(longitude), float(latitude))
        item["distance"] = geodesic((float(latitude), float(longitude)), (39.91092, 116.41338)).km

        target_point = ','.join([longitude, latitude])
        item["gaode"] = walks(target_point, '116.276554,39.904581')

        item["floor"] = detailText.xpath("//div[@class='jlyoubai fl jlyoubai1']/div[@class='jlquannei']/p[@class='houseinfor2']/text()").extract_first()
        item["size"] = detailText.xpath("//div[@class='jlyoubai fl jlyoubai2']/div[@class='jlquannei']/p[@class='houseinfor1']/text()").extract_first()
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