# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time
import os
'''
1 获取全部合约信息(交易日历)
2 将合约信息分为50etfo和300etfo并生成两个新表
3 以合约信息的ts_code为索引 获取单个期权的日数据
4 观看实例来确定如何进行数据清洗
华夏上证50ETF期权2009认购3
华夏上证50ETF期权1712认沽2.209
华泰柏瑞沪深300ETF期权2009认沽4
华泰柏瑞沪深300ETF期权2001认购3.60
50etf[0:11]名称opt_code [11:15]到期月maturity_date [15:17]类型call_put [17:]执行价exercise_price
300etf[0:14]名称opt_code [14:18]到期月maturity_date [18:20]类型call_put [20:]执行价exercise_price
'''
pro = ts.pro_api('7ae709d0ba634357a957ca4798150dabecc3da0ac3b6829c4624765a')

# 获取合约信息并保存到本地
'''
df = pro.opt_basic(exchange='SSE')
df.to_csv(path_or_buf='./Data/basic.csv', index=0, encoding='gbk')

basic = pd.read_csv(filepath_or_buffer='./Data/basic.csv', encoding='gbk', index_col=0).sort_values(ascending=True, by='ts_code')
sz50etf_o = basic.loc[basic['opt_code'] == 'OP510050.SH']
hs300etf_o = basic.loc[basic['opt_code'] == 'OP510300.SH']
sz50etf_o.to_csv(path_or_buf='./Data/basic_50.csv', encoding='gbk')
hs300etf_o.to_csv(path_or_buf='./Data/basic_300.csv', encoding='gbk')
'''
# tick接口(已废弃)
'''
start_day = datetime.datetime(2019,12,23).date()
end_day = datetime.datetime(2019,12,24).date()

df = pro.ft_tick('IH')
df.to_csv(path_or_buf='./Data/{date}.csv'.format(date=start_day), index=0)
'''
sz50etf_o = pd.read_csv(filepath_or_buffer='./Data/basic_50.csv', encoding='gbk')
sz50etf_o_list = sz50etf_o['ts_code'].values
hs300etf_o = pd.read_csv(filepath_or_buffer='./Data/basic_300.csv', encoding='gbk')
hs300etf_o_list = hs300etf_o['ts_code'].values
# sz50etf期权日数据
'''
for ts_code in sz50etf_o_list:
    df = pro.opt_daily(ts_code=ts_code)
    time.sleep(0.4)
    df.to_csv(path_or_buf='./Data/option/{code}.csv'.format(code=ts_code[:-3]), index=0, encoding='gbk')
    print(ts_code)
'''
# hs300etf期权日数据
'''
for ts_code in hs300etf_o_list:
    df = pro.opt_daily(ts_code=ts_code)
    time.sleep(0.4)
    df.to_csv(path_or_buf='./Data/option/{code}.csv'.format(code=ts_code[:-3]), index=0, encoding='gbk')
    print(ts_code)
'''
# 合并单只期权数据为面板数据
'''
df_all = pd.DataFrame
for ts_code in sz50etf_o_list:
    df = pd.read_csv(filepath_or_buffer='./Data/option/{code}.csv'.format(code=ts_code[:-3]),index_col=0)
    if ts_code == sz50etf_o_list[0]:
        df_all = df
    else:
        df_all = pd.concat([df_all,df])
df_all.to_csv(path_or_buf='./Data/daily_50etfo.csv')

for ts_code in hs300etf_o_list:
    df = pd.read_csv(filepath_or_buffer='./Data/option/{code}.csv'.format(code=ts_code[:-3]),index_col=0)
    if ts_code == hs300etf_o_list[0]:
        df_all = df
    else:
        df_all = pd.concat([df_all,df])
df_all.to_csv(path_or_buf='./Data/daily_300etfo.csv')
'''
daily_50etfo = pd.read_csv(filepath_or_buffer='./Data/daily_50etfo.csv',index_col=0)
daily_300etfo = pd.read_csv(filepath_or_buffer='./Data/daily_300etfo.csv',index_col=0)


