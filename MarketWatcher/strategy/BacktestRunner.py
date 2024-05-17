# -*- coding: utf-8 -*-

from math import inf
import os
import datetime
import time
import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import TimeSeriesSplit
from multiprocessing import Manager, Process
from importlib import import_module
from backtesting import Backtest
from backtesting._util import _Indicator
from backtesting._stats import compute_stats
from database.OHLCVTableManager import fetch_OHLCV, fetch_symbols
from database.StatsTableManager import StatsTableManager
from database.TradeTableManager import TradeTableManager
from logging import getLogger
logger = getLogger(__name__)

class HtmlBuilder(object):
    def __init__(self):
        self.stats_file_name = 'stats_aggregated_trans.csv'
        self.export_file_name = 'index.html'
        self.import_path_backtest = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', 'backtest')
        self.import_path_forwardtest = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', 'forwardtest')
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
            'Win Rate [%]',
            'optimized',
            'plot',
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
            self.build_dataframe(is_backtest=True)
            self.build_dataframe(is_backtest=False)

        export_file = os.path.join(self.export_path, self.export_file_name)
        table_html = self.df[self.output_columns].to_html(escape=False, justify='center', float_format='{:10.2f}'.format)
        html = self.html_index_template.format(table_html)
        html = html.replace('dataframe', 'dataframe sortable')
        with open(export_file, mode='w') as fp:
            fp.write(html)
    
    def build_dataframe(self, is_backtest=True):
        import_path = self.import_path_backtest if is_backtest else self.import_path_forwardtest
        file_path = os.path.join(import_path, self.stats_file_name)
        df = pd.read_csv(file_path, index_col=0)
        buff = []
        for idx in df.index:
            tmp = self.parse(idx, is_backtest)
            self.parse_stats_html(idx, import_path)
            buff.append(tmp)

        df_parsed= pd.DataFrame(buff)
        df = df.merge(df_parsed, left_index=True, right_on='title')
        dt_now = datetime.datetime.now()
        df['updated'] = dt_now.strftime('%Y-%m-%d %H:%M:%S')

        if self.df is None:
            self.df = df
        else:
            self.df = pd.concat([self.df, df], ignore_index=True)

        self.df.index += 1

    def parse_stats_html(self, title, import_path):
        stats_file = os.path.join(import_path, f'stats_{title}.csv')
        trades_file = os.path.join(import_path, f'trades_{title}.csv')
        df_stats = pd.read_csv(stats_file, index_col=0)
        df_trades = pd.read_csv(trades_file)
        df_trades.index += 1
        html = self.html_stats_template.format(
            df_stats.to_html(escape=False, justify='center', float_format='{:,.2f}'.format),
            df_trades.to_html(escape=False, justify='center', float_format='{:,.2f}'.format))

        with open(os.path.join(import_path, f'stats_{title}.html'), mode='w') as fp:
            fp.write(html)

        # os.remove(stats_file)
        # os.remove(trades_file)

    @staticmethod
    def parse(title, is_backtest=True):
        buff = title.split('_')
        test_type = 'backtest' if is_backtest else 'forwardtest'
        result = {
            'title': title,
            'strategy': buff[0],
            'exchange_name': buff[1],
            'asset': buff[2],
            'freq': buff[3],
            'optimized': (('_opt_' in title) or not is_backtest),
            'plot': f'<a href="./MarketWatcher/output/{test_type}/plot_{title}.html" target="_blank" rel="noopener noreferrer">{test_type}</a>',
            'stats': f'<a href="./MarketWatcher/output/{test_type}/stats_{title}.html" target="_blank" rel="noopener noreferrer">table</a>'
        }
        return result

class BacktestRunner(object):
    def __init__(self, exchange_name, symbol, rule, strategy, cash=10e6, margin=1.0, commission=0.002, max_tries=30,
                 exclusive_orders=True, from_date='1950-01-01', to_date='2100-12-31', drop_na=False, df=None, maximize='SQN'):
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
        self.max_tries = max_tries
        self.maximize = maximize
        self.stats_mgr = StatsTableManager()
        # self.trade_mgr = TradeTableManager()

    def initialize_strategy(self):
        if self.df is None:
            self.df = fetch_OHLCV(self.exchange_name, self.symbol, self.rule, self.from_date, self.to_date, self.drop_na)
        self.backtest = Backtest(self.df, self.strategy, cash=self.cash, margin=self.margin,
                                 commission=self.commission, exclusive_orders=self.exclusive_orders)
        
    @staticmethod
    def fetch_all_symbols():
        return fetch_symbols()

    def insert_stats(self, strategy_name, test_type, optimized):
        export_idx = list(range(0, 29)) + [32]
        insert_stats = self.stats[export_idx]
        insert_stats['_parameter'] = str(insert_stats['_parameter'])
        for idx in insert_stats.index:
            if '[%]' in idx:
                insert_stats[idx] *= 0.01

            if not (isinstance(insert_stats[idx], float) and isinstance(insert_stats[idx], int)):
                insert_stats[idx] = str(insert_stats[idx])

        timestamp = time.time()
        datetime_str = datetime.datetime.fromtimestamp(int(str(timestamp)[0:10])).strftime('%Y-%m-%d %H:%M:%S')
        insert_data = [
            timestamp, datetime_str,
            strategy_name, self.exchange_name, self.symbol, self.rule, int(optimized), test_type] + insert_stats.tolist()
        self.stats_mgr.insert(insert_data)

    def insert_trade(self, trade_df, strategy_name, test_type, optimized):
        timestamp = time.time()
        trade = trade_df.copy(deep=True)
        trade['uodatetime'] = timestamp
        trade['datetime'] = datetime.datetime.fromtimestamp(int(str(timestamp)[0:10])).strftime('%Y-%m-%d %H:%M:%S')
        trade['strategy_name'] = strategy_name
        trade['exchange'] = self.exchange_name
        trade['product_code'] = self.symbol
        trade['freq'] = self.rule
        trade['test_type'] = test_type
        trade['optimized'] = int(optimized)

    @staticmethod
    def train_test_splits(df, n_fold=5, moving_window=False):
        size = len(df) // n_fold
        for i in range(size, n_fold * size, size):
            if moving_window:
                # moving window
                train_data = df.iloc[(i-size):i]
            else:
                # expanding window
                train_data = df.iloc[:i]

            if i == ((n_fold - 1) * size):
                test_data = df.iloc[i:]
            else:
                test_data = df.iloc[i:i + size]

            yield train_data, test_data

    @staticmethod
    def train_test_split2(df, n_splits=5, max_train_size=None, test_size=None):
        splitter = TimeSeriesSplit(n_splits=n_splits, max_train_size=max_train_size, test_size=test_size)
        return splitter.split(df)

    def compute_merged_stats(self, stats_list, risk_free_rate=0.0):
        trades = pd.DataFrame()
        equity = pd.Series(dtype=float)
        indicators = None
        params = {}
        for stats in stats_list:
            if len(stats['_trades']) > 0:
                trades = pd.concat([trades, stats['_trades']], ignore_index=True)
            equity = pd.concat([equity, stats['_equity_curve']['Equity']])
            key = '{}_{}'.format(str(stats['Start']), str(stats['End']))
            params[key] = stats['_parameter']

            tmp = """
            if indicators is None:
                indicators = stats._strategy._indicators
            else:
                for i in range(len(stats._strategy._indicators)):
                    ind = stats._strategy._indicators[i]
                    ind_df = pd.concat([indicators[i].df, ind.df])

                    if isinstance(ind_df, pd.DataFrame):
                        ind_df = ind_df.values.T

                    # if np.argmax(ind_df.shape) == 0:
                    #    ind_df = ind_df.T

                    ind_index = indicators[i]._opts['index'].append(ind._opts['index'])
                    indicators[i] = _Indicator(
                        ind_df,
                        name=ind.name,
                        plot=ind._opts['plot'],
                        overlay=ind._opts['overlay'],
                        color=ind._opts['color'],
                        scatter=ind._opts['scatter'],
                        index=ind_index
                    )

                    """
        stats_list[0]._strategy._indicators = indicators
        equity = equity.values
        results = compute_stats(
            trades=trades,
            equity=equity,
            ohlc_data=self.df,
            risk_free_rate=risk_free_rate,
            strategy_instance=stats_list[0]._strategy
        )
        results['_parameter'] = params
        return results

    def run_forwardtest(self, method='skopt', n_fold=5):
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
            stats_insmaple = []
            stats = self.backtest.run()
            initial_cash = self.backtest._broker.keywords['cash']
            prev_test_final_cash = initial_cash
            params_range = stats._strategy.optimization_parameter
            df_org = self.df

            is_first = True
            for train_data, test_data in self.train_test_splits(self.df, n_fold=n_fold):
                # train run
                self.df = train_data
                self.initialize_strategy()
                self.optimization_method = method
                self.backtest._broker.keywords['cash'] = initial_cash
                stats, heatmap  = self.backtest.optimize(**params_range,
                    return_heatmap=True, maximize=self.maximize, method=method, max_tries=self.max_tries)
                stats['_parameter'] = stats['_strategy'].get_used_parameter()
                if is_first:
                    self.stats.append(stats)
                    prev_test_final_cash = stats['Equity Final [$]']
                    is_first = False

                # test run
                stats_insmaple.append(stats)
                # opt_strategy_params = stats._strategy._params
                opt_strategy_params = stats['_strategy'].get_used_parameter()
                self.df = test_data
                self.initialize_strategy()
                self.backtest._broker.keywords['cash'] = prev_test_final_cash
                stats = self.backtest.run(**opt_strategy_params)
                stats['_trades']['EntryBar'] += len(train_data)
                stats['_trades']['ExitBar'] += len(train_data)
                stats['_parameter'] = stats['_strategy'].get_used_parameter()
                prev_test_final_cash = stats['Equity Final [$]']
                self.stats.append(stats)

            self.df = df_org
            results = self.compute_merged_stats(self.stats)
            results._strategy._indicators = []
            self.stats = results
            self.backtest._results = results
            self.backtest._data = df_org
        except Exception as e:
            logger.error(e.args)
            logger.error('{} forward test failed.'.format(log_str))

    def run(self, run_optimization=False, run_forwardtest=False, method='skopt', export_to_db=False, **params):
        try:
            if not self.initialized:
                self.initialize_strategy()

            log_str = '[{}][{}][{}][{}]'.format(
                self.backtest._strategy.__name__,
                self.exchange_name,
                self.symbol,
                self.rule)

            logger.info('{} backtest started.'.format(log_str))
            self.stats = self.backtest.run(**params)
            self.stats['_parameter'] = self.stats['_strategy'].get_used_parameter()
            self.export(export_to_db=export_to_db)
            logger.info('{} backtest completed.'.format(log_str))

            if run_optimization:
                logger.info('{}[{}] backtest started.'.format(log_str, 'opt'))
                params = self.stats._strategy.optimization_parameter
                self.optimization_method = method
                self.stats, self.heatmap = self.backtest.optimize(
                    **params, return_heatmap=True, maximize=self.maximize, method=method, max_tries=self.max_tries)
                self.stats['_parameter'] = self.stats['_strategy'].get_used_parameter()
                self.export(True, export_to_db=export_to_db)
                log_str += '[opt]'
                logger.info('{} backtest completed.'.format(log_str))

            if run_forwardtest:
                logger.info('{} forwardtest started.'.format(log_str))
                self.run_forwardtest()
                self.export(is_backtest=False, export_to_db=export_to_db)
                logger.info('{} forwardtest completed.'.format(log_str))

        except Exception as e:
            logger.error(e.args)
            logger.error('{} backtest failed.'.format(log_str))

    def export(self, is_optimization=False, is_backtest=True, export_to_db=False):
        if self.stats is None:
            self.run()
        
        test_type = 'backtest' if is_backtest else 'forwardtest'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', test_type)
        strategy_name = self.stats['_strategy'].strategy_name
        strategy_name = f'{strategy_name}_{self.exchange_name}_{self.symbol}_{self.rule}'
        if is_optimization:
            strategy_name += f'_opt_{self.optimization_method}'

        trades = self.stats['_trades'].copy(deep=True)
        trades['ReturnPct'] *= 100.0
        trades.to_csv(os.path.join(output_path, f'trades_{strategy_name}.csv'), index=False)
        idx = list(range(0, 29)) + [32]
        if export_to_db:
            self.insert_stats(strategy_name, test_type, is_optimization if is_backtest else True)
        else:
            # self.insert_stats(strategy_name, test_type, is_optimization if is_backtest else True)            
           self.stats[idx].to_csv(os.path.join(output_path, f'stats_{strategy_name}.csv'), header=[strategy_name])

        resample = True

        title_prefix = '[{}]'.format('Backtesting' if is_backtest else 'Forwardtesting')
        title = title_prefix + strategy_name
        self.backtest.plot(filename=os.path.join(output_path, f'plot_{strategy_name}.html'), title=title, show_stats=True, show_trades=True,
                           resample=resample, open_browser=False, plot_return=False, reverse_indicators=False)
        if is_optimization and self.heatmap is not None:
            self.heatmap.to_csv(os.path.join(output_path, f'heatmap_{strategy_name}.csv'))

    @staticmethod
    def aggregate_test_result(stats_file_list, is_backtest=True):
        test_type = 'backtest' if is_backtest else 'forwardtest'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', test_type)
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

def run_single_scenario(exchange_name, symbol, rule, strategy, cash, margin, commission, exclusive_orders, from_date, to_date, drop_na, run_optimize, run_forwardtest):
    maximize = 'Avg. Drawdown [%]'
    maximize = 'SQN'
    maximize = lambda stats: -inf if stats['Avg. Drawdown [%]'] < -30 else stats['SQN']
    BacktestRunner(
        exchange_name=exchange_name,
        symbol=symbol, 
        rule=rule,
        strategy=strategy,
        cash=cash,
        margin=margin,
        commission=commission,
        exclusive_orders=exclusive_orders,
        from_date=from_date,
        to_date=to_date,
        drop_na=drop_na,
        maximize=maximize).run(run_optimization=run_optimize, run_forwardtest=run_forwardtest)

def run_backtest_scenario(use_test_config=False):
    yaml_file_name = 'config_test.yml' if use_test_config else 'config.yml'
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
            for st_sub in st_val:
                for ast in assets:
                    kwargs = ast
                    imported_module = import_module(f'strategy.{st}.{st_key}')
                    kwargs['strategy'] = getattr(imported_module, st_sub)
                    kwargs['from_date'] = kwargs['from_date'] if 'from_date' in kwargs.keys() else '1950-01-01'
                    kwargs['to_date'] = kwargs['to_date'] if 'to_date' in kwargs.keys() else '2100-12-31'
                
                    stats_file_name = 'stats_{}_{}_{}_{}.csv'.format(
                        st_sub, kwargs['exchange_name'], kwargs['symbol'], kwargs['rule'])
                    stats_file_list.append(stats_file_name)
                    if kwargs['run_optimize']:
                        stats_file_name = 'stats_{}_{}_{}_{}_{}.csv'.format(
                        st_sub, kwargs['exchange_name'], kwargs['symbol'], kwargs['rule'], 'opt_skopt')
                        stats_file_list.append(stats_file_name)

                    if is_parallel:
                        process = Process(target=run_single_scenario, kwargs=kwargs)
                        process.start()
                        process_list.append(process)
                    else:
                        run_single_scenario(
                            kwargs['exchange_name'], kwargs['symbol'], kwargs['rule'], kwargs['strategy'], kwargs['cash'], kwargs['margin'],
                            kwargs['commission'], kwargs['exclusive_orders'], kwargs['from_date'], kwargs['to_date'], kwargs['drop_na'],
                            kwargs['run_optimize'], kwargs['run_forwardtest'])

    if is_parallel:
        for process in process_list:
            process.join()

    BacktestRunner.aggregate_test_result(stats_file_list, is_backtest=True)
    BacktestRunner.aggregate_test_result(stats_file_list, is_backtest=False)
    HtmlBuilder().export()
