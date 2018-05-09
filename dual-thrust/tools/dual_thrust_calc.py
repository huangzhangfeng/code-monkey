'''
用二八策略计算当前应该持有的指数
'''
# -*- coding: utf-8 -*-

import datetime as dt
import tushare as ts

s1 = '000300.XSHG'
s2 = '000905.XSHG'
cons = None
retry = 3
while cons is None and retry > 0:
    cons = ts.get_apis()
    retry -= 1

two_months_ago = dt.date.today() - dt.timedelta(60)
rlt1 = ts.bar(code = s1, conn = cons, start_date = two_months_ago.isoformat(), freq = 'd', asset = 'INDEX')

rlt2 = ts.bar(code = s2, conn = cons, start_date = two_months_ago.isoformat(), freq = 'd', asset = 'INDEX')

s1delta = (rlt1.iloc[0]['close']-rlt1.iloc[20]['close'])/rlt1.iloc[20]['close']
s2delta = (rlt2.iloc[0]['close']-rlt2.iloc[20]['close'])/rlt2.iloc[20]['close']

s1delta_prev = (rlt1.iloc[1]['close']-rlt1.iloc[21]['close'])/rlt1.iloc[21]['close']
s2delta_prev = (rlt2.iloc[1]['close']-rlt2.iloc[21]['close'])/rlt2.iloc[21]['close']

hold_prev = None
if s1delta_prev < 0 and s2delta_prev < 0:
    hold_prev = 'cash'
elif s1delta_prev > s2delta_prev:
    hold_prev = s1
else:
    hold_prev = s2

hold = None
if s1delta < 0 and s2delta < 0:
    hold = 'cash'
elif s1delta > s2delta:
    hold = s1
else:
    hold = s2

if hold_prev != hold:
    print('调仓：' + hold_prev + ' -> ' + hold)
else:
    print('持仓：' + hold)

ts.close_apis(cons)
