# scripts/stock_daily.py

from apps.system.jobs.stocks.baseic import stat_all_index
from apps.system.jobs.stocks.guess import runGuess
import sys
import logging


def run(*args):
    logger = logging.getLogger('log')
    logger.info('每天执行')
    logger.info(sys.argv)

    stat_all_index()
    # runGuess()
