# Create your tasks here
from __future__ import absolute_import, unicode_literals

import logging
import sys
from celery import shared_task
from apps.system.jobs.stocks.baseic import stat_all_index
from apps.system.jobs.stocks.guess import runGuess

@shared_task
def daily():
    logger = logging.getLogger('log')
    logger.info('股票每天任务')
    logger.error(sys.argv)

    # 获取股票信息
    stat_all_index()
    runGuess()

@shared_task
def daily_guess():
    logger = logging.getLogger('log')
    logger.info('================= 获取股票信息 ===================')
    logger.info(sys.argv)

    # 获取股票信息
    runGuess()

@shared_task
def guess():
    runGuess()
