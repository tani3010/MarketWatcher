# -*- coding: utf-8 -*-

import os
import timeit
import yaml
import logging
from logging import getLogger, config
from run_update_db import update_db
from run_backtest import run_backtest

def main():
    try:
        logger = getLogger(__name__)
        yaml_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config_logging.yml'))
        config.dictConfig(yaml.safe_load(open(yaml_path, 'r', encoding='utf-8').read()))

        logger.info('update DB started.')
        start = timeit.default_timer()
        update_db()
        stop = timeit.default_timer()
        logger.info('completed in {}[sec].'.format(stop - start))

        logger.info('backtest started.')
        start = timeit.default_timer()
        run_backtest()
        stop = timeit.default_timer()
        logger.info('completed in {}[sec].'.format(stop - start))

    except Exception as e:
        logger.error(e.args)

if __name__ == '__main__':
    main()