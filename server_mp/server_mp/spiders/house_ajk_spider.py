import random
import re

import scrapy
import random
import time
from datetime import datetime
import os
import math
import json
import requests
from geopy.distance import geodesic

from server_mp.items import HouseItem

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

class HouseAnjuke(scrapy.Spider):
    name = "house_ajk"
    start_urls = [
        'https://bj.zu.anjuke.com/ditie/dt6-x1-fx2-s2042/',
    ]
    base_url = 'https://bj.zu.anjuke.com/ditie/dt6-x1-fx2-s2042-p{0}/'

    allowed_domains = ['bj.zu.anjuke.com']

    def __init__(self, *args, **kwargs):
        self.page_num = 1

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }

    def start_requests(self):
        # 一些user_agent
        USER_AGENT = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        ]

        headers = {
            'User-Agent': random.choice(USER_AGENT)
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        item = HouseItem()
        house_div = response.xpath("//div[@class='zu-itemmod']")
	
	# for each in [house_div[0]]:
        for each in house_div:
            item['source'] = 'ajk'
            item['title'] = each.xpath(".//div[@class='zu-info']//h3//a//b/text()").extract()[0].strip()

            pattern = r'\/([0-9].*)\?'
            url = each.xpath(".//div[@class='zu-info']//h3//a/@href").extract_first()
            item['house_code'] = re.findall(pattern, url)[0]
            item['url'] = f"https://bj.zu.anjuke.com/fangyuan/{item['house_code']}"

            item['price'] = each.xpath(".//div[@class='zu-side']//p//strong//b/text()").extract()[0].strip()
            item['img'] = each.xpath('.//a[@class="img"]/img/@src').extract_first()
            item["size"] = each.xpath(".//div[@class='zu-info']//p[@class='details-item tag']//b[position()=3]/text()").extract()[0].strip()
            item["floor"] = each.xpath(".//div[@class='zu-info']//p[@class='details-item tag']/text()").extract()[4].strip()
            item['address'] = each.xpath(".//div[@class='zu-info']//address[@class='details-item']/text()").extract()[1].strip()
            item['distance'] = each.xpath(".//div[@class='zu-info']//p[@class='details-item bot-tag']//span[last()]/text()").extract()[
                0].strip()
            # item['name'] = each.xpath(".//div[@class='zu-info']//address[@class='details-item']//a/text()").extract()[
            #     0].strip()

            now = datetime.now()
            item["operate_time"] = now.strftime("%Y-%m-%d")
            item["ctime"] = now.strftime("%Y-%m-%d %H:%M:%S")
            item["utime"] = now.strftime("%Y-%m-%d %H:%M:%S")

            if url:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                print(url)
                sec = random.uniform(1, 3)
                time.sleep(sec)

                # 请求详情页
                yield scrapy.Request(
                    url=item['url'],
                    callback=self.parse_detail,
                    headers=headers,
                    meta={"item": item}
                )

        # 计算下一页的 URL
        self.page_num += 1
        if self.page_num > 6:
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
        latText = response.xpath('//script/text()').extract()[1]

        pattern = 'lng: "(.*)"'
        longitude = re.findall(pattern, latText)
        if len(longitude) > 0:
            longitude = longitude[0]

        pattern = 'lat: "(.*)",'
        latitude = re.findall(pattern, latText)
        if len(latitude) > 0:
            latitude = latitude[0]
        item['longitude'] = longitude
        item['latitude'] = latitude

        item["longitude"], item["latitude"] = bdToGaoDe(float(longitude), float(latitude))
        item["distance"] = geodesic((float(latitude), float(longitude)), (39.91092, 116.41338)).km
        
        target_point = ','.join([longitude, latitude])
        item["gaode"] = walks(target_point, '116.276554,39.904581')

        # 维护时间
        # item["operate_time"] = response.xpath("//div[@class='content__subtitle']/text()").extract_first()
        # item["operate_time"] = self.get_number_str(item['operate_time'])
        # item["size"] = response.xpath(
        #     "//div[@class='content__article__info']/ul/li[position()=2]/text()").extract_first()
        # item["size"] = self.get_number_str(item['size'])
        # now = datetime.now()
        # item["ctime"] = now.strftime("%Y-%m-%d %H:%M:%S")

        yield item  # 对返回的数据进行处理
