'''
策略回测文件
'''
# -*- coding: utf-8 -*-
import os
from rqalpha import run_file

STRATEGY_FILE = './two_eight.py'
SCENES = [
    {'name': 'ten_years', 'start_date': '2008-05-24', 'end_date': '2018-05-24'},
    {'name': 'bull_market_2015', 'start_date': '2013-06-30', 'end_date': '2015-06-30'},
    {'name': 'bear_market_2007', 'start_date': '2007-10-31', 'end_date': '2008-12-31'},
    {'name': 'bear_market_2015', 'start_date': '2015-05-30', 'end_date': '2016-05-31'},
    {'name': 'monkey_market_2008_14', 'start_date': '2008-10-31', 'end_date': '2014-04-30'},
    {'name': 'monkey_market_2016_18', 'start_date': '2016-02-29', 'end_date': '2018-05-01'}
]
OUTPUTS_DIR = './outputs/'
RESULTS_DIR = OUTPUTS_DIR + 'results/'

if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

config = {
    "base": {
        "start_date": "",
        "end_date": "",
        "securities": ['stock'],
        "stock_starting_cash": 1000000,
        "benchmark": "000001.XSHG"
    },
    "extra": {
        "log_level": "info",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": False,
            "output_file": "",
            "report_save_path": "",
            "plot_save_file": ""
        },
        "sys_simulation": {
            "enabled": True,
            "slippage": 0.002
        }
    }
}
for scene in SCENES:
    config['base']['start_date'] = scene['start_date']
    config['base']['end_date'] = scene['end_date']
    config['mod']['sys_analyser']['output_file'] = RESULTS_DIR  + scene['name'] + '.pkl'
    config['mod']['sys_analyser']['report_save_path'] = RESULTS_DIR + scene['name']
    config['mod']['sys_analyser']['plot_save_file'] = RESULTS_DIR + scene['name'] + '.png'

    if not os.path.exists(RESULTS_DIR + scene['name']):
        os.makedirs(RESULTS_DIR + scene['name'])
    run_file(STRATEGY_FILE, config)
