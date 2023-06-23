# scripts/tu_share_stk_factor.py

# 导入tushare
import os
import time

import tushare as ts

# 初始化pro接口
from sqlalchemy import create_engine

pro = ts.pro_api(os.environ.get("TOKEN"))

engine = create_engine(os.environ.get("CREAT_ENGINE"))


def run(*args):
    # 拉取数据
    df = pro.trade_cal(**{
        "exchange": "",
        "cal_date": "",
        "start_date": 20220901,
        "end_date": "",
        "is_open": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "cal_date",
    ])

    for date in df['cal_date'].values:
        df = pro.stk_factor(trade_date=date)

        # df = get_stk_factor(trade_date=date)
        df.to_sql('tu_share_stk_factor', engine, if_exists='replace')


def get_stk_factor(ts_code='', trade_date=''):
    for _ in range(3):
        try:
            df = pro.stk_factor(ts_code=ts_code, trade_date=trade_date)
        except:
            time.sleep(1)
        else:
            return df
