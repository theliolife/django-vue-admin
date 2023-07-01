import os
import json
from datetime import datetime
import pandas as pd
from django.db import models, connection
from django.core import serializers
from django.forms.models import model_to_dict
import libs.common as common


# scripts/test.py
class MtPrice(models.Model):
    # 约束内容为长度16,name唯一,列名自定义为'name'
    name = models.CharField(max_length=100, db_column='name')
    date = models.DateField(db_column='date')
    t_price = models.CharField(max_length=100, db_column='today_price')
    y_price = models.CharField(max_length=100, db_column='yesterday_price')
    create_time = models.DateTimeField('创建时间', auto_now_add=True, db_column='ctime')
    update_time = models.DateTimeField('更新时间', auto_now=True, db_column='utime')

    # 添加元信息改变表的名称
    class Meta:
        db_table = 'mt_price'

    @staticmethod
    def getInfo():
        cursor = connection.cursor()
        cursor.execute(f"select * from mt_price limit 10")
        lists = MtPrice.dict_fetch_all(cursor)
        return {'data': lists}

    @staticmethod
    def getList(date):
        cursor = connection.cursor()
        cursor.execute(f"select * from mt_price where date = '%s'" % date)
        lists = MtPrice.dict_fetch_all(cursor)
        return {'data': lists}

    @staticmethod
    def getListByName(date, name):
        cursor = connection.cursor()
        cursor.execute(f"select * from mt_price where date = '%s' AND name like '%s'" % (date, f"%{name}%"))
        lists = MtPrice.dict_fetch_all(cursor)
        return {'data': lists}

    @staticmethod
    def dict_fetch_all(cursor):
        """
        将游标返回的所有结果转换为字典列表
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def saveAll(data):
        variables = list(data[0].keys())
        dataframe = pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

        current_date = datetime.now().strftime("%Y-%m-%d")
        first_person = MtPrice.objects.raw(f"select id,name from mt_price where date = '%s'" % current_date)[0:1]
        if first_person:
            return True
        return common.insert_db(dataframe, "mt_price", True, "`name`,`id`")
