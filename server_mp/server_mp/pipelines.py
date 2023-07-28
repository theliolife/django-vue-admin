#coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import pymysql
# from scrapy.pipelines.images import ImagesPipeline
import scrapy

class ServerMpPipeline:
    def process_item(self, item, spider):
        return item


# class Pipline(ImagesPipeline):
#     # 将图片的src进行请求下载,
#     def get_media_requests(self, item, info):
#         # print("item的src是",item["src"])
#         # 这里不需要回调函数,直接进行请求,meta可以把前面的参数给传下去,比如传自定义的文件名
#         yield scrapy.Request(item["src"], meta=item)
#
#     # 执行下一个即将执行的管道类,所以如果没有其他管道存储,也可以不写这个方法
#     def item_completed(self, results, item, info):
#         return item
#
#     # 设定存储文件名,存储路径的父路径在setting里设置 IMAGES_STORE 字段
#     def file_path(self, request, response=None, info=None, *, item=None):
#         # return item["fname"]   直接把item里的文件名返回
#
#         # 这里是把url后面的xxx.jpg截取作为文件名返回保存
#         f_name = request.url.split("/")[-1]
#         return f_name


class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(
            host=os.environ.get("DB_HOST"),  # 数据库IP地址
            port=int(os.environ.get("DB_PORT")),  # 数据库端口
            db=os.environ.get("DB_DATABASE"),  # 数据库名
            user=os.environ.get("DB_USERNAME"),  # 数据库用户名
            passwd=os.environ.get("DB_PASSWORD"),  # 数据库密码
            charset='utf8',  # 编码方式
        )
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if spider.name == 'house' or spider.name == 'house_5i5j' or spider.name == 'house_ajk':

            values = (
                item['source'],
                item['house_code'],
                item['price'],
                item['title'],
                item['url'],
                item['img'],
                item['operate_time'],
                item['size'],
                item['floor'],
                item['longitude'],
                item['latitude'],
                item['distance'],
                item['gaode'],
                item['ctime'],
            )
            # # 编写insert sql语句，这里是数据库中已经有表了
            sql = 'INSERT INTO sp_house (`source`, `house_code`, `price`, `title`, `url`, `img`, `operate_time`, `size`, `floor`, `longitude`, `latitude`, `distance`, `gaode`, `ctime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                # 执行sql语句
                self.cursor.execute(sql, values)
                # 提交sql语句
                self.db.commit()
            except:
                exit(1)
                # 发生错误时回滚
                self.db.rollback()
            # 返回item
            return item

    def close_spider(self, spider):
        self.db.close()
