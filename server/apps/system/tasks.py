# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import sys
import logging


@shared_task
def show():
    logger = logging.getLogger('log')
    logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}')
    logger.error('请求出错-{}-task')
    logger.error(sys.argv)

    print('ok')
