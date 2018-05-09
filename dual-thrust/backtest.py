'''
策略回测文件
'''
# -*- coding: utf-8 -*-
import os
from rqalpha import run_file

STRATEGY_FILE = './dual_thrust.py'
SCENES = [
    {'name': 'ten_years', 'start_date': '2008-05-01', 'end_date': '2018-05-01'},
    {'name': 'bull_market_2015', 'start_date': '2013-06-30', 'end_date': '2015-06-30'},
    {'name': 'bear_market_2007', 'start_date': '2007-10-31', 'end_date': '2008-12-31'},
    {'name': 'bear_market_2015', 'start_date': '2015-05-30', 'end_date': '2016-05-31'},
    {'name': 'monkey_market_2008_14', 'start_date': '2008-10-31', 'end_date': '2014-04-30'},
    {'name': 'monkey_market_2016_18', 'start_date': '2016-02-29', 'end_date': '2018-05-01'}
]

if not os.path.exists('./results'):
    os.makedirs('./results')

config = {
    "base": {
        "start_date": "",
        "end_date": "",
        "securities": ['stock'],
        "stock_starting_cash": 100000,
        "benchmark": "000905.XSHG"
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
        }
    }
}
for scene in SCENES:
    config['base']['start_date'] = scene['start_date']
    config['base']['end_date'] = scene['end_date']
    config['mod']['sys_analyser']['output_file'] = './results/' + scene['name'] + '.pkl'
    config['mod']['sys_analyser']['report_save_path'] = './results/' + scene['name']
    config['mod']['sys_analyser']['plot_save_file'] = './results/' + scene['name'] + '.png'

    if not os.path.exists('./results/' + scene['name']):
        os.makedirs('./results/' + scene['name'])
    run_file(STRATEGY_FILE, config)
