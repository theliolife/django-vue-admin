#coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import pymysql

class ServerMpPipeline:
    def process_item(self, item, spider):
        return item


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
        if spider.name == 'house':

            values = (
                item['house_code'],
                item['price'],
                item['title'],
                item['url'],
                item['img'],
                item['operate_time'],
                item['size'],
                item['ctime'],
            )
            # # 编写insert sql语句，这里是数据库中已经有表了
            sql = 'INSERT INTO sp_house (`house_code`, `price`, `title`, `url`, `img`, `operate_time`, `size`, `ctime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                print('-----------------------------')
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