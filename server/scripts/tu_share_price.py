# scripts/tu_share_price_daily.py

# 导入tushare
import os
import time

import tushare as ts
import pandas as pd

# 初始化pro接口
from sqlalchemy import create_engine

pro = ts.pro_api(os.environ.get("TU_SHARE_TOKEN"))

engine = create_engine('mysql://'+os.environ.get("DB_USERNAME")+':'+os.environ.get("DB_PASSWORD")+'@'+os.environ.get("DB_HOST")+'/'+os.environ.get("DB_HOST")+'?charset=utf8')

def run(*args):
    # 拉取数据
    df = pro.trade_cal(**{
        "exchange": "",
        "cal_date": "",
        "start_date": 2023325,
        "end_date": "",
        "is_open": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "cal_date",
    ])

    for date in df['cal_date'].values:
        print(date)
        df = get_daily(trade_date=date)
        df.to_sql('tu_share_price_daily', engine, if_exists='append', index=False)

        df = get_weekly(trade_date=date)
        df.to_sql('tu_share_price_weekly', engine, if_exists='append', index=False)

        df = get_monthly(trade_date=date)
        df.to_sql('tu_share_price_monthly', engine, if_exists='append', index=False)


def get_daily(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = pro.daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df


def get_weekly(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = pro.weekly(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df


def get_monthly(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = pro.monthly(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.monthly(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df