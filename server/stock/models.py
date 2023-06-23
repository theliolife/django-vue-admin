import os
import json
from datetime import datetime

from django.db import models, connection
from django.core import serializers
from django.forms.models import model_to_dict

# scripts/test.py
class Test(models.Model):

    # 约束内容为长度16,name唯一,列名自定义为'name'
    code = models.CharField(max_length=100, unique=True, db_column='code')
    name = models.CharField(max_length=100, unique=True, db_column='name')
    # p_age = models.IntegerField(default=18, db_column='age')
    # # False代表男,默认为男
    # p_sex = models.BooleanField(default=False, db_column='sex')
    # # 默认参数
    # name = models.CharField(max_length=100)
    #
    # create_time = models.DateTimeField('创建时间', default=datetime.now())
    # update_time = models.DateTimeField('更新时间', default=datetime.now)
    #
    # # create_time_tow = models.DateTimeField('创建时间', auto_now_add=True)
    # # update_time_tow = models.DateTimeField('更新时间', auto_now=True)

    # 添加元信息改变表的名称
    class Meta:
        db_table = 'accounts'

    @staticmethod
    def displayCount():
        print(os.environ.get("DB_USERNAME"))

    @staticmethod
    def getInfo2():
        # cursor = connection.cursor()
        # cursor.execute(f"select * from stock_zh_a_spot_em limit 10")  # 缺少FROM子句
        # list = cursor.fetchall()

        first_person = Test.objects.raw(f"select code,name from stock_zh_a_spot_em")[0:1]
        # first_person = model_to_dict(first_person)
        list = []
        for item in first_person:
            list.append([item.month])
        data = {'data': list}
        return data
        # return serializers.serialize("json", first_person)

    @staticmethod
    def getInfo():
        cursor = connection.cursor()
        cursor.execute(f"select * from stock_zh_a_spot_em limit 10")
        lists = Test.dict_fetch_all(cursor)
        return {'data': lists}

    @staticmethod
    def dict_fetch_all(cursor):
        """
        将游标返回的所有结果转换为字典列表
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]