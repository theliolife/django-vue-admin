# scripts/tu_share_stock_base.py

# 导入tushare
import os

import tushare as ts
import pandas as pd

# 初始化pro接口
from sqlalchemy import create_engine

pro = ts.pro_api(os.environ.get("TU_SHARE_TOKEN"))

engine = create_engine('mysql://'+os.environ.get("DB_USERNAME")+':'+os.environ.get("DB_PASSWORD")+'@'+os.environ.get("DB_HOST")+'/'+os.environ.get("DB_HOST")+'?charset=utf8')


def run(*args):
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
