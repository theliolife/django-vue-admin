# scripts/tu_share_stock_base.py

# 导入tushare
import os

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
        "start_date": "",
        "end_date": "",
        "is_open": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "exchange",
        "cal_date",
        "is_open",
        "pretrade_date"
    ])
    print(df)

    # 追加数据到现有表
    df.to_sql('tu_share_trade_cal', engine, if_exists='replace', index_label='id')
