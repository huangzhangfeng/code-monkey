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
    context.n = 3
    context.k1 = 0.5
    context.k2 = 0.5
    context.hold = 'cash'
    update_universe(context.stock)

def handle_bar(context, bar_dict):
    '''
    交易函数
    '''
    hist_h = history_bars(context.stock, context.n, '1d', 'high')
    hist_l = history_bars(context.stock, context.n, '1d', 'low')
    hist_c = history_bars(context.stock, context.n, '1d', 'close')
    hh = np.max(hist_h)
    hc = np.max(hist_c)
    lc = np.min(hist_c)
    ll = np.min(hist_l)
    dt_range = np.max([hh - lc, hc - ll])
    growth = hist_c[-1] - hist_c[-2]

    action = 'hold'
    top_bound = context.k1 * dt_range
    bottom_bound = context.k2 * dt_range * -1
    import pdb; pdb.set_trace()
    if growth > top_bound:
        action = 'buy'
    elif growth < bottom_bound:
        action = 'sell'
    else:
        action = 'hold'

    if action == 'buy' and context.hold == 'cash':
        order_target_percent(context.stock, 1)
        context.hold = context.stock
    elif action == 'sell' and context.hold == context.stock:
        order_target_percent(context.stock, 0)
        context.hold = 'cash'
    else:
        return
