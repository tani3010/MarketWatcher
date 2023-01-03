# -*- coding: utf-8 -*-

import os
import datetime
import numpy as np
import pandas as pd
import yaml
from multiprocessing import Manager, Process
from importlib import import_module
from backtesting import Backtest
from backtesting._util import _Indicator
from backtesting._stats import compute_stats
from database.OHLCVTableManager import fetch_OHLCV, fetch_symbols
from logging import getLogger
logger = getLogger(__name__)

class HtmlBuilder(object):
    def __init__(self):
        self.stats_file_name = 'stats_aggregated_trans.csv'
        self.export_file_name = 'index.html'
        self.import_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', 'backtest')
        self.export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir)
        self.output_columns = [
            'strategy',
            'exchange_name',
            'asset',
            'freq',
            'Start',
            'End',
            'Return [%]',
            'Buy & Hold Return [%]',
            'optimized',
            'backtest',
            'stats',
            'updated'
        ]
        self.df = None
        self.html_index_template = '''
            <!DOCTYPE html>
            <html>
            <head>
              <meta charset="UTF-8">
              <title>Backtesting</title>
            </head>
            <body>
              <h1>Backtesting</h1>
              {} <!-- table -->
            </body>
            <link href="https://cdn.jsdelivr.net/gh/tofsjonas/sortable/sortable.min.css" rel="stylesheet" />
            <script type="text/javascript" src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable/sortable.min.js"></script>
            </html>
        '''
        self.html_stats_template = '''
            <!DOCTYPE html>
            <html>
            <style>
              table {{text-align: right;}}
              table thead th {{text-align: center;}}
            </style>
            <head>
              <meta charset="UTF-8">
              <title>Backtesting</title>
            </head>
            <body>
              <h1>stats</h1>
              {} <!-- table -->
              <h1>trades</h1>
              {} <!-- table -->
            </body>
            </html>
        '''
        
    def export(self):
        if self.df is None:
            self.build_dataframe()

        export_file = os.path.join(self.export_path, self.export_file_name)
        table_html = self.df[self.output_columns].to_html(escape=False, justify='center', float_format='{:10.2f}'.format)
        html = self.html_index_template.format(table_html)
        html = html.replace('dataframe', 'dataframe sortable')
        with open(export_file, mode='w') as fp:
            fp.write(html)
    
    def build_dataframe(self):
        file_path = os.path.join(self.import_path, self.stats_file_name)
        df = pd.read_csv(file_path, index_col=0)

        buff = []
        for idx in df.index:
            tmp = self.parse(idx)
            self.parse_stats_html(idx)
            buff.append(tmp)

        df_parsed= pd.DataFrame(buff)
        df = df.merge(df_parsed, left_index=True, right_on='title')
        dt_now = datetime.datetime.now()
        df['updated'] = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        self.df = df

    def parse_stats_html(self, title):
        stats_file = f'stats_{title}.csv'
        trades_file = f'trades_{title}.csv'
        df_stats = pd.read_csv(os.path.join(self.import_path, stats_file), index_col=0)
        df_trades = pd.read_csv(os.path.join(self.import_path, trades_file))
        html = self.html_stats_template.format(
            df_stats.to_html(escape=False, justify='center', float_format='{:,.2f}'.format),
            df_trades.to_html(escape=False, justify='center', float_format='{:,.2f}'.format))

        with open(os.path.join(self.import_path, f'stats_{title}.html'), mode='w') as fp:
            fp.write(html)

    @staticmethod
    def parse(title):
        buff = title.split('_')
        result = {
            'title': title,
            'strategy': buff[0],
            'exchange_name': buff[1],
            'asset': buff[2],
            'freq': buff[3],
            'optimized': '_opt_' in title,
            'backtest': f'<a href="./MarketWatcher/output/backtest/plot_{title}.html" target="_blank" rel="noopener noreferrer">plot</a>',
            'stats': f'<a href="./MarketWatcher/output/backtest/stats_{title}.html" target="_blank" rel="noopener noreferrer">table</a>'
        }
        return result

class BacktestRunner(object):
    def __init__(self, exchange_name, symbol, rule, strategy, cash=10e6, margin=1.0, commission=0.002,
                 exclusive_orders=False, from_date='1950-01-01', to_date='2100-12-31', drop_na=False, df=None):
        self.exchange_name = exchange_name
        self.symbol = symbol
        self.rule = rule
        self.cash = float(cash)
        self.margin = margin
        self.commission = commission
        self.exclusive_orders = exclusive_orders
        self.optimization_method = None
        self.stats = None
        self.heatmap = None
        self.df = df
        self.from_date = from_date
        self.to_date = to_date
        self.strategy = strategy
        self.initialized = False
        self.drop_na = drop_na

    def initialize_strategy(self):
        if self.df is None:
            self.df = fetch_OHLCV(self.exchange_name, self.symbol, self.rule, self.from_date, self.to_date, self.drop_na)
        self.backtest = Backtest(self.df, self.strategy, cash=self.cash, margin=self.margin,
                                 commission=self.commission, exclusive_orders=self.exclusive_orders)
        
    @staticmethod
    def fetch_all_symbols():
        return fetch_symbols()

    @staticmethod
    def train_test_splits(df, n_fold=5):
        size = len(df) // n_fold
        for i in range(size, n_fold * size, size):
            train_data = df.iloc[:i]
            test_data = df.iloc[i:i + size]
            yield train_data, test_data

    def compute_merged_stats(self, stats_list, risk_free_rate=0.0):
        trades = None
        equity = None
        indicators = None
        for stats in stats_list:
            trades = stats['_trades'] if trades is None else trades.append(stats['_trades'])
            tmp_equity = stats['_equity_curve']['Equity']
            equity = tmp_equity if equity is None else equity.append(tmp_equity)
            if indicators is None:
                indicators = stats._strategy._indicators
            else:
                for i in range(len(stats._strategy._indicators)):
                    ind = stats._strategy._indicators[i]
                    indicators[i] = _Indicator(
                        pd.concat([indicators[i].df, ind.df]),
                        name=ind.name,
                        plot=ind._opts['plot'],
                        overlay=ind._opts['overlay'],
                        color=ind._opts['color'],
                        scatter=ind._opts['scatter'],
                        index=indicators[i]._opts['index'].append(ind._opts['index'])
                )

        stats_list[0]._strategy._indicators = indicators
        results = compute_stats(
            trades=trades,
            equity=equity,
            ohlc_data=self.df,
            risk_free_rate=risk_free_rate,
            strategy_instance=stats_list[0]._strategy
        )
        return result

    def run_forward_test(self, method='skopt'):
        try:
            if self.df is None:
                self.df = fetch_OHLCV(self.exchange_name, self.symbol, self.rule)
            self.initialize_strategy()
            log_str = '[{}][{}][{}][{}]'.format(
                self.backtest._strategy.__module__,
                self.exchange_name,
                self.symbol,
                self.rule)
            self.stats = []
            stats = self.backtest.run()
            params_range = stats._strategy.optimization_parameter
            for train_data, test_data in self.train_test_splits(self.df):
                self.df = train_data
                self.initialize_strategy()
                self.optimization_method = method
                stats = self.backtest.optimize(**params_range,
                    return_heatmap=False, maximize='SQN', method=method)

                opt_strategy_params = stats._strategy._params
                self.df = test_data
                self.initialize_strategy()
                stats = self.backtest.run(**opt_strategy_params)
                self.stats.append(stats)

            result = self.compute_merged_stats(self.stats)

            print(self.stats)
        except Exception as e:
            logger.error(e.args)
            logger.error('{} forward test failed.'.format(log_str))

    def run(self, run_optimization=False, method='skopt', **params):
        try:
            if not self.initialized:
                self.initialize_strategy()

            log_str = '[{}][{}][{}][{}]'.format(
                self.backtest._strategy.__module__,
                self.exchange_name,
                self.symbol,
                self.rule)

            logger.info('{} backtest started.'.format(log_str))
            self.stats = self.backtest.run(**params)
            self.export()
            logger.info('{} backtest completed.'.format(log_str))

            if run_optimization:
                logger.info('{}[{}] backtest started.'.format(log_str, 'opt'))
                params = self.stats._strategy.optimization_parameter
                self.optimization_method = method
                self.stats, self.heatmap = self.backtest.optimize(
                    **params, return_heatmap=True, maximize='SQN', method=method)
                # maximize = ('SQN', 'Equity Final [$]')
                # method = ('grid', 'skopt')
                self.export(True)
                log_str += '[opt]'
                logger.info('{} backtest completed.'.format(log_str))

        except Exception as e:
            logger.error(e.args)
            logger.error('{} backtest failed.'.format(log_str))

    def export(self, is_optimization=False):
        if self.stats is None:
            self.run()
        
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', 'backtest')
        strategy_name = self.stats['_strategy'].strategy_name
        suffix = f'{strategy_name}_{self.exchange_name}_{self.symbol}_{self.rule}'
        if is_optimization:
            suffix += f'_opt_{self.optimization_method}'
        strategy_name = suffix
        self.stats['_trades'].to_csv(os.path.join(output_path, f'trades_{suffix}.csv'), index=False)
        self.stats[0:27].to_csv(os.path.join(output_path, f'stats_{suffix}.csv'), header=[strategy_name])
        resample = '1W' if len(self.df) >= 10000 else True
        self.backtest.plot(filename=os.path.join(output_path, f'plot_{suffix}.html'),
                           resample=False, open_browser=False, plot_return=False, reverse_indicators=False)
        if is_optimization and self.heatmap is not None:
            self.heatmap.to_csv(os.path.join(output_path, f'heatmap_{suffix}.csv'))

    @staticmethod
    def aggregate_backtest_result(stats_file_list):
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', 'backtest')
        df = None
        for file_name in stats_file_list:
            full_path = os.path.join(output_path, file_name)
            if not os.path.isfile(full_path):
                continue
            df_tmp = pd.read_csv(full_path, index_col=0)
            df = df_tmp if df is None else df.join(df_tmp)
        output_file = os.path.join(output_path, 'stats_aggregated.csv')
        df.to_csv(output_file)

        output_file = os.path.join(output_path, 'stats_aggregated_trans.csv')
        df.T.to_csv(output_file)

def run_single_scenario(exchange_name, symbol, rule, strategy, cash, margin, commission, exclusive_orders, from_date, to_date, drop_na, run_optimize):
    BacktestRunner(exchange_name, symbol, rule, strategy, cash, margin, commission, exclusive_orders, from_date, to_date, drop_na).run(run_optimize)

def run_backtest_scenario():
    yaml_file_name = 'config.yml'
    yaml_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'config', yaml_file_name))
    yaml_obj = None
    with open(yaml_path) as file:
        yaml_obj = yaml.safe_load(file)

    assets = yaml_obj['BacktestSetting']['asset']
    strats = yaml_obj['BacktestSetting']['strategy']

    is_parallel = yaml_obj['BacktestSetting']['run_parallel']
    process_list = []
    stats_file_list = []
    for st in strats.keys():
        for st_key, st_val in strats[st].items():
            for ast in assets:
                kwargs = ast
                imported_module = import_module(f'strategy.{st}.{st_key}') 
                kwargs['strategy'] = getattr(imported_module, st_val[0])
                kwargs['from_date'] = kwargs['from_date'] if 'from_date' in kwargs.keys() else '1950-01-01'
                kwargs['to_date'] = kwargs['to_date'] if 'to_date' in kwargs.keys() else '2100-12-31'
                
                stats_file_name = 'stats_{}_{}_{}_{}.csv'.format(
                    st_val[0], kwargs['exchange_name'], kwargs['symbol'], kwargs['rule'])
                stats_file_list.append(stats_file_name)
                if kwargs['run_optimize']:
                    stats_file_name = 'stats_{}_{}_{}_{}_{}.csv'.format(
                    st_val[0], kwargs['exchange_name'], kwargs['symbol'], kwargs['rule'], 'opt_skopt')
                    stats_file_list.append(stats_file_name)

                if is_parallel:
                    process = Process(target=run_single_scenario, kwargs=kwargs)
                    process.start()
                    process_list.append(process)
                else:
                    run_single_scenario(
                        kwargs['exchange_name'], kwargs['symbol'], kwargs['rule'], kwargs['strategy'], kwargs['cash'], kwargs['margin'],
                        kwargs['commission'], kwargs['exclusive_orders'], kwargs['from_date'], kwargs['to_date'], kwargs['drop_na'],
                        kwargs['run_optimize'])

    if is_parallel:
        for process in process_list:
            process.join()

    BacktestRunner.aggregate_backtest_result(stats_file_list)
    HtmlBuilder().export()
