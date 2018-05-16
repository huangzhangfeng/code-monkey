'''
策略运行文件
'''
# -*- coding: utf-8 -*-

from rqalpha.api import logger, order_target_percent, history_bars

STOCKS = ['000300.XSHG', '000905.XSHG']

def init(context):
    '''
    策略初始化
    '''
    logger.info("init")
    context.stocks = STOCKS
    #当前持仓品种，取值为STOCKS里的值以及cash
    context.hold = 'cash'
    #下一步调仓品种，取值范围同hold，取值为None时表示持仓不调
    context.trade = None
    #趋势判断窗口，往前看20个交易日
    context.window_size = 20
    #记录最近一次的调仓日期
    #大多数基金存在7日内赎回1.5%的交易手续费
    #所以两次调仓间隔大于7天才调仓
    context.trade_date = None

def fund_trading(context):
    '''
    基金交易函数，T日发出交易信号，T+1日卖出，T+2日买入
    '''
    if context.trade is None:
        return
    log_str = '[' + context.now.isoformat() + ']'
    if context.hold != 'cash' and context.trade == 'cash':
        order_target_percent(context.hold, 0)
        log_str += 'sell ' + context.hold
        context.hold = 'cash'
        context.trade = None
    elif context.hold == 'cash' and context.trade != 'cash':
        order_target_percent(context.trade, 0.99)
        log_str += 'buy ' + context.trade
        context.hold = context.trade
        context.trade = None
    elif context.hold != 'cash' and context.trade != 'cash':
        order_target_percent(context.hold, 0)
        log_str += 'sell ' + context.hold
        context.hold = 'cash'
    else:
        log_str += 'unkown trading signal'
        logger.error(log_str)
        return
    logger.info(log_str)

def handle_bar(context, bar_dict):
    '''
    交易函数
    '''
    if context.trade is not None:
        fund_trading(context)
        return
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
    if context.trade_date is not None:
        holding_days = context.now - context.trade_date
        if holding_days.days < 8:
            return
    context.trade = trading
    context.trade_date = context.now
    logger.info(log_str)
