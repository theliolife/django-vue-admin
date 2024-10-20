# scripts/stock_daily.py

from apps.system.jobs.stocks.baseic import stat_all_index
from apps.system.jobs.stocks.guess import runGuess
from apps.system.jobs.stocks.quarter import runQuarter
import os
import sys
import logging
from datetime import datetime

from maotai.imaotai import price
from server.settings import LOG_PATH
import akshare as ak



def run(*args):
    price.run()
    
    # stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20210907',
    #                                         adjust="")
    # print(stock_zh_a_hist_df)
    # exit(1)
    #
    # print(sys.argv)
    # logger = logging.getLogger('log')
    # logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}')
    # logger.error('请求出错-{}')

    # stat_all_index()
    # runGuess()
    # runQuarter()
