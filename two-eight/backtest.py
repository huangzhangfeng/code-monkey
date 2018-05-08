'''
策略回测文件
'''
# -*- coding: utf-8 -*-
import os
from rqalpha import run_file

if not os.path.exists('./results'):
    os.makedirs('./results')
if not os.path.exists('./results/quick_glance'):
    os.makedirs('./results/quick_glance')
if not os.path.exists('./results/bull_market_2015'):
    os.makedirs('./results/bull_market_2015')
CONFIG = {
    "base": {
        "start_date": "2008-05-01",
        "end_date": "2018-05-01",
        "securities": ['stock'],
        "stock_starting_cash": 100000,
        "benchmark": "000001.XSHG"
    },
    "extra": {
        "log_level": "verbose",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": False,
            "output_file": "./results/quick_glance.pkl",
            "report_save_path": "./results/quick_glance",
            "plot_save_file": "./results/quick_glace.png"
        }
    }
}
run_file('./two_eight.py', CONFIG)

CONFIG = {
    "base": {
        "start_date": "2013-06-30",
        "end_date": "2015-06-30",
        "securities": ['stock'],
        "stock_starting_cash": 100000,
        "benchmark": "000001.XSHG"
    },
    "extra": {
        "log_level": "verbose",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": False,
            "output_file": "./results/bull_market_2015.pkl",
            "report_save_path": "./results/bull_market_2015",
            "plot_save_file": "./results/bull_market_2015.png"
        }
    }
}
run_file('./two_eight.py', CONFIG)
