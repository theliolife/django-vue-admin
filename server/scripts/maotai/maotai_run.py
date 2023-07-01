# scripts/stock_daily.py

import sys
import logging
from maotai.imaotai import base


def run(*args):
    logger = logging.getLogger('log')
    logger.info('i茅台每天执行')
    logger.info(sys.argv)

    base.run()