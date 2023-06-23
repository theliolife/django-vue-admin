# scripts/stock_daily.py

from apps.system.stocks.baseic import stat_all_index
import os
import logging
from datetime import datetime
from server.settings import LOG_PATH


def run(*args):
    # logger = logging.getLogger('log')
    # logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}')
    # logger.error('请求出错-{}')

    stat_all_index()
