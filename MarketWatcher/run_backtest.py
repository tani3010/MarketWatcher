# -*- coding: utf-8 -*-

from strategy.BacktestRunner import run_backtest_scenario

def run_backtest(use_test_config=False):
    run_backtest_scenario(use_test_config)

if __name__ == '__main__':
    run_backtest()