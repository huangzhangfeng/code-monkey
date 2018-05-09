'''
策略运行文件
'''
# -*- coding: utf-8 -*-
import numpy as np
from rqalpha.api import update_universe, logger, order_target_percent, history_bars

def init(context):
    '''
    策略初始化
    '''
    logger.info("init")
    context.stock = '000905.XSHG'
    context.n = 10
    context.k1 = 0.2
    context.k2 = 0.3
    context.hold = 'cash'
    update_universe(context.stock)

def handle_bar(context, bar_dict):
    '''
    交易函数
    '''
    hist_h = history_bars(context.stock, context.n, '1d', 'high')
    hist_l = history_bars(context.stock, context.n, '1d', 'low')
    hist_c = history_bars(context.stock, context.n, '1d', 'close')
    #import pdb; pdb.set_trace()
    hh = np.max(hist_h)
    hc = np.max(hist_c)
    lc = np.min(hist_c)
    ll = np.min(hist_l)
    dt_range = np.max([hh - lc, hc - ll])

    today_growth = bar_dict[context.stock].close -bar_dict[context.stock].open
    if context.hold == 'cash' and today_growth > context.k1 * dt_range:
        order_target_percent(context.stock, 1)
        context.hold = context.stock
    elif context.hold == context.stock and today_growth < context.k2 * dt_range * -1:
        order_target_percent(context.stock, 0)
        context.hold = 'cash'
    else:
        return
