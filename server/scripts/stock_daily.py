# scripts/stock_daily.py

from apps.system.jobs.stocks.baseic import stat_all_index
from apps.system.jobs.stocks.guess import runGuess
from apps.system.jobs.stocks.quarter import runQuarter
import os
import sys
import logging
from datetime import datetime
from server.settings import LOG_PATH


def run(*args):
    print(sys.argv)
    # logger = logging.getLogger('log')
    # logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}')
    # logger.error('请求出错-{}')

    # stat_all_index()
    runGuess()
    # runQuarter()
