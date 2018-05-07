'''
策略运行文件
'''
# -*- coding: utf-8 -*-

from rqalpha.api import update_universe, logger, order_target_percent, history_bars, scheduler

STOCKS = ['000300.XSHG', '000905.XSHG', '000012.XSHG']

def init(context):
    '''
    策略初始化
    '''
    logger.info("init")
    context.stocks = STOCKS
    update_universe(context.stocks)
    context.trading = None
    context.hold = None
    scheduler.run_weekly(handle_bar_weekly, 4)


def handle_bar_weekly(context, bar_dict):
    s1 = history_bars(context.stocks[0], 21, '1d','close')
    s2 = history_bars(context.stocks[1], 21, '1d','close')
    s1delta = (s1[-1] - s1[0]) / s1[0]
    s2delta = (s2[-1] - s2[0]) / s2[0]
    log_str = '沪深300涨幅: ' + str(round(s1delta, 2)) + ' 中证500涨幅: ' + str(round(s2delta, 2))
    hold = None
    if s1delta is not None and s2delta is not None:
        if s1delta < 0 and s2delta < 0:
            hold = context.stocks[2]
        elif s1delta > s2delta:
            hold = context.stocks[0]
        else:
            hold = context.stocks[1]
    if hold is not None:
        context.trading = hold
    else:
        context.trading = context.hold
    if context.trading is None or context.trading == context.hold:
        return
    if context.hold is not None:
        order_target_percent(context.hold, 0)
        log_str += ' sell ' + context.hold
    order_target_percent(context.trading, 1)
    log_str += ' buy ' + context.trading
    context.hold = context.trading
    logger.info(log_str)

def before_trading(context):
    '''
    交易前执行的事件
    '''
    return

def handle_bar(context, bar_dict):
    '''
    交易时间执行
    '''
    return
