'''
策略运行文件
'''
# -*- coding: utf-8 -*-

from rqalpha.api import update_universe, logger, order_target_percent, history_bars

def init(context):
    '''
    策略初始化
    '''
    logger.info("init")
    context.stock = '000905.XSHG'
    update_universe(context.stock)

def handle_bar(context, bar_dict):
    '''
    交易函数
    '''
    return

def before_trading(context):
    '''
    交易前执行的事件
    '''
    return
