'''
策略运行文件
'''
# -*- coding: utf-8 -*-

from rqalpha.api import (
    logger,
    order_target_percent,
    history_bars,
    scheduler,
)

STOCKS = ['000300.XSHG', '000905.XSHG']

def init(context):
    '''
    策略初始化
    '''
    logger.info("init")
    context.stocks = STOCKS
    #当前持仓品种，取值为STOCKS里的值以及cash
    context.hold = 'cash'
    #趋势判断窗口，往前看20个交易日
    context.window_size = 20
    scheduler.run_weekly(handle_bar_weekly, tradingday=-1)

def handle_bar(context, bar_dict):
    pass

def handle_bar_weekly(context, bar_dict):
    '''
    交易函数
    '''
    hist_s1 = history_bars(context.stocks[0],
                           context.window_size + 1, '1d', 'close')
    hist_s2 = history_bars(context.stocks[1],
                           context.window_size + 1, '1d', 'close')
    curr_s1 = bar_dict[context.stocks[0]].close
    curr_s2 = bar_dict[context.stocks[1]].close
    logger.debug('s1:' + str(hist_s1))
    logger.debug('s2:' + str(hist_s2))
    s1delta = (curr_s1  - hist_s1[0]) / hist_s1[0]
    s2delta = (curr_s2  - hist_s2[0]) / hist_s2[0]
    log_str = '[' + context.now.isoformat() + ']'
    log_str += '沪深300 ' + str(hist_s1[0]) + '->' + str(curr_s1)
    log_str += ' 涨幅: ' + str(round(s1delta, 3))
    log_str += ' 中证500 '+ str(hist_s2[0]) + '->' + str(curr_s2)
    log_str += ' 涨幅: ' + str(round(s2delta, 3))
    trading = None
    if s1delta is not None and s2delta is not None:
        if s1delta < 0 and s2delta < 0:
            trading = 'cash'
        elif s1delta > s2delta:
            trading = context.stocks[0]
        else:
            trading = context.stocks[1]
    if trading is None or trading == context.hold:
        return
    if context.hold != 'cash':
        order_target_percent(context.hold, 0)
        log_str += ' sell ' + context.hold
    if trading != 'cash':
        order_target_percent(trading, 0.99)
        log_str += ' buy ' + trading
    context.hold = trading
    logger.info(log_str)
