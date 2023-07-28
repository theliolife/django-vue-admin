# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ServerMpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HouseNeedItem(scrapy.Item):
    # define the fields for your item here like:
    source = scrapy.Field()
    title = scrapy.Field()
    room = scrapy.Field()
    size = scrapy.Field()
    far = scrapy.Field()
    name = scrapy.Field()
    area = scrapy.Field()
    pic = scrapy.Field()
    money = scrapy.Field()


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    source = scrapy.Field()
    house_code = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    operate_time = scrapy.Field()
    size = scrapy.Field()
    floor = scrapy.Field()
    address = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    distance = scrapy.Field()
    gaode = scrapy.Field()
    ctime = scrapy.Field()
    utime = scrapy.Field()
