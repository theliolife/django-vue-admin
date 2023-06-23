# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import tushare as ts
import pandas as pd

# 导入tushare
import os

# 初始化pro接口
from sqlalchemy import create_engine

pro = ts.pro_api(os.environ.get("TU_SHARE_TOKEN"))

engine = create_engine(os.environ.get("CREAT_ENGINE"))


@shared_task
def stock_base():
    # 拉取数据
    df = pro.stock_basic(**{
        "ts_code": "",
        "name": "",
        "exchange": "",
        "market": "",
        "is_hs": "",
        "list_status": "",
        "limit": "",
        "offset": ""
    }, fields=[
        'ts_code',
        'symbol',
        'name',
        'area',
        'industry',
        'fullname',
        'enname',
        'cnspell',
        'market',
        'exchange',
        'curr_type',
        'list_status',
        'list_date',
        'delist_date',
        'is_hs',
    ])

    df = pd.DataFrame(df, columns=['ts_code',
                                   'symbol',
                                   'name',
                                   'area',
                                   'industry',
                                   'fullname',
                                   'enname',
                                   'cnspell',
                                   'market',
                                   'exchange',
                                   'curr_type',
                                   'list_status',
                                   'list_date',
                                   'delist_date',
                                   'is_hs'])

    # 存入数据库
    # df.to_sql('stock_basic', engine)

    # 追加数据到现有表
    # df.to_sql('tu_share_stock_basic', engine, if_exists='append', index=False)
    df.to_sql('tu_share_stock_basic', engine, if_exists='replace', index_label='id')