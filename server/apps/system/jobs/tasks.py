# Create your tasks here
from __future__ import absolute_import, unicode_literals

import logging
import sys
from celery import shared_task
from apps.system.jobs.stocks.baseic import stat_all_index
from apps.system.jobs.stocks.guess import runGuess

@shared_task
def daily():
    # logger = logging.getLogger('log')
    # logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}')
    # logger.error('请求出错-{}')
    # logger.error(sys.argv)

    # 获取股票信息
    stat_all_index()

@shared_task
def daily_guess():
    # logger = logging.getLogger('log')
    # logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}')
    # logger.error('请求出错-{}')
    # logger.error(sys.argv)

    # 获取股票信息
    runGuess()

@shared_task
def guess():
    runGuess()
