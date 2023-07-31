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

    scrapy_sp.start_spider('server_mp', 'house')


@shared_task
def wiwj():
    logger = logging.getLogger('log')
    logger.info('请求成功！ scrapy_5i5j爬虫每日的任务')
    logger.info(sys.argv)

    scrapy_sp.start_spider('server_mp', 'house_5i5j')

@shared_task
def ajk():
    logger = logging.getLogger('log')
    logger.info('请求成功！ scrapy_ajk爬虫每日的任务')
    logger.info(sys.argv)

    scrapy_sp.start_spider('server_mp', 'house_ajk')


@shared_task
def guess():
    print("爬虫每日任务3")
