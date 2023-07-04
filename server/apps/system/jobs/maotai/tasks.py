# Create your tasks here
from __future__ import absolute_import, unicode_literals

from maotai.imaotai import base, price

import logging
import sys
from celery import shared_task

@shared_task
def daily():
    logger = logging.getLogger('log')
    logger.info('茅台每天任务')
    logger.info(sys.argv)

    price.run()

@shared_task
def price():
    logger = logging.getLogger('log')
    logger.info('茅台每天任务')
    logger.info(sys.argv)

    price.run()

@shared_task
def reservation():
    logger = logging.getLogger('log')
    logger.info('茅台每天预约')
    logger.info(sys.argv)

    base.run()
