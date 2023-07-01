# scripts/maotai/maotai_price.py

import sys
import logging
from maotai.imaotai import price


def run(*args):
    logger = logging.getLogger('log')
    logger.info('茅台价格每天执行')
    logger.info(sys.argv)

    price.run()