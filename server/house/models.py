import os
import json
from datetime import datetime

from django.db import models, connection
from django.core import serializers
from django.forms.models import model_to_dict


class House(models.Model):
    house_code = models.CharField(max_length=100, unique=True, db_column='house_code')
    title = models.CharField(max_length=100, unique=True, db_column='title')
    ctime = models.DateTimeField('创建时间', default=datetime.now(), db_column='ctime')
    utime = models.DateTimeField('更新时间', default=datetime.now, db_column='utime')

    # # create_time_tow = models.DateTimeField('创建时间', auto_now_add=True)
    # # update_time_tow = models.DateTimeField('更新时间', auto_now=True)

    # 添加元信息改变表的名称
    class Meta:
        db_table = 'sp_house'

    @staticmethod
    def displayCount():
        print(os.environ.get("DB_USERNAME"))

    @staticmethod
    def dashboard():
        res = {}
        cursor = connection.cursor()

        operate_time = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(f"select count(*) as total from sp_house where operate_time = '{operate_time}'")
        res['current_total'] = House.dict_fetch_all(cursor)

        operate_time = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            f"select operate_time,count(*) as total from sp_house group by operate_time order by operate_time desc limit 30")
        res['statistic'] = House.dict_fetch_all(cursor)
        return {'data': res}

    @staticmethod
    def list(operate_time=''):
        cursor = connection.cursor()

        if operate_time == '':
            operate_time = datetime.now().strftime("%Y-%m-%d")
        operate_time_str = datetime.now().strftime("%Y%m%d")

        cursor.execute(f"select * from sp_house where operate_time = '%s' or operate_time = '%s'" % (operate_time, operate_time_str))
        res = House.dict_fetch_all(cursor)

        return {'data': res}

    @staticmethod
    def dict_fetch_all(cursor):
        """
        将游标返回的所有结果转换为字典列表
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
