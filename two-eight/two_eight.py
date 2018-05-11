'''
策略运行文件
'''
# -*- coding: utf-8 -*-

from rqalpha.api import update_universe, logger, order_target_percent, history_bars

STOCKS = ['000300.XSHG', '000905.XSHG']

def init(context):
    '''
    策略初始化
    '''
    logger.info("init")
    context.stocks = STOCKS
    update_universe(context.stocks)
    context.hold = None
    context.window_size = 20

def handle_bar(context, bar_dict):
    '''
    交易函数
    '''
    s1 = history_bars(context.stocks[0], context.window_size + 1, '1d','close')
    s2 = history_bars(context.stocks[1], context.window_size + 1, '1d','close')
    logger.debug('s1:' + str(s1))
    logger.debug('s2:' + str(s2))
    s1delta = (s1[-1] - s1[0]) / s1[0]
    s2delta = (s2[-1] - s2[0]) / s2[0]
    log_str = '沪深300 ' + str(s1[0]) + '->' + str(s1[-1]) + ' 涨幅: ' + str(round(s1delta, 3)) + ' 中证500 '+ str(s2[0]) + '->' + str(s2[-1]) +  ' 涨幅: ' + str(round(s2delta, 3))
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
    if context.hold is not None and context.hold != 'cash':
        order_target_percent(context.hold, 0)
        log_str += ' sell ' + context.hold
    if trading != 'cash':
        order_target_percent(trading, 1)
        log_str += ' buy ' + trading
    context.hold = trading
    logger.info(log_str)
