# Create your tasks here
from __future__ import absolute_import, unicode_literals

from libs import scrapy_sp

import logging
import sys
from celery import shared_task
from apps.system.jobs.stocks.baseic import stat_all_index
from apps.system.jobs.stocks.guess import runGuess

@shared_task
def daily():
    logger = logging.getLogger('log')
    logger.info('请求成功！ scrapy_爬虫每日的任务')
    logger.info(sys.argv)

    res = scrapy_sp.get_status()
    print("scrapy_爬虫每日de任务")
    print(res)

@shared_task
def daily_guess():
    # logger = logging.getLogger('log')
    # logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}')
    # logger.error('请求出错-{}')
    # logger.error(sys.argv)

    # 获取股票信息
    print("爬虫每日任务2")

@shared_task
def guess():
    print("爬虫每日任务3")
