# scripts/stock_daily.py

import sys
import logging
from maotai.imaotai import login


def run(*args):
    logger = logging.getLogger('log')
    logger.info('i茅台每天执行')
    logger.info(sys.argv)

    login.run()