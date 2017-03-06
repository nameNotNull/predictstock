# -*- coding: UTF-8 -*-
import tensorflow as tf

import tushare as ts

import datetime


test_stock = '000001'
start_date = datetime.date(2014, 3,8)
end_date = datetime.date(2017, 2, 23)
test_start_date = datetime.date(2016,1, 25)
def datelist(start_date, end_date):
    #start_date = datetime.date(*start)
    #end_date = datetime.date(*end)
    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result
trading_days = datelist(start_date,end_date)
start_date_index = trading_days.index("%04d%02d%02d" % (start_date.year, start_date.month, start_date.day))
end_date_index = trading_days.index("%04d%02d%02d" % (end_date.year, end_date.month, end_date.day))

test_start_index = trading_days.index("%04d%02d%02d" % (test_start_date.year, test_start_date.month, test_start_date.day))
#x_all中保存所有的特征信息
#y_all中保存所有的标签信息（要预测的对象）
x_all = []
y_all = []
x_test_all = []
y_test_all = []

def getXData(index, period):
    #获取股票数据
    start_day =  datetime.datetime.strptime(trading_days[index],"%Y%m%d")
    second_day =  datetime.datetime.strptime(trading_days[index+period],"%Y%m%d")
    end_day = datetime.datetime.strptime(trading_days[index+period+1],"%Y%m%d")

    start_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))

    second_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day),end="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day))
    end_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day),end="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day))
    if start_day_stock_data.empty  :
       #print "当天的数据为空",start_day, "end", end_day
        return
    #大盘指数
    index_sh = ts.get_hist_data('sh',start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))
    if index_sh.empty :
        print "当天大盘数据为空***********************",start_day
        return 
    index_sz = ts.get_hist_data('sz',start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))
    index_cyb = ts.get_hist_data('cyb',start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))

    i=1
    while   second_day_stock_data.empty:
        #print "后一天的数据为空 +++++++", second_day
        second_day = datetime.datetime.strptime(trading_days[index+period+i],"%Y%m%d")
        second_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day),end="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day))
        i +=1

    while   end_day_stock_data.empty:
        #print "后两天的数据为空 +++++++", end_day
        end_day = datetime.datetime.strptime(trading_days[index+period+i],"%Y%m%d")
        end_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day),end="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day))
        i +=1
    feature = []
    feature.append(start_day_stock_data['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['v_ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['v_ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['v_ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['turnover']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(second_day_stock_data['price_change']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['volume']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['open']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['close']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['high']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['low']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['p_change']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['ma5']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['ma10']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['ma20']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['v_ma5']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['v_ma10']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['v_ma20']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['turnover']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(index_sh['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['v_ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['v_ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['v_ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['v_ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['v_ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['v_ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    label = []
    if end_day_stock_data['price_change']["%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day)] > 0:
        label.append(0)
        label.append(1)
    else :
        label.append(1)
        label.append(0)
    print "今天日期",start_day
    x_all.append(feature)
    y_all.append(label)

def getTestData(index, period):
    #获取股票数据
    start_day =  datetime.datetime.strptime(trading_days[index],"%Y%m%d")
    second_day =  datetime.datetime.strptime(trading_days[index+period],"%Y%m%d")
    end_day = datetime.datetime.strptime(trading_days[index+period+1],"%Y%m%d")

    start_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))

    second_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day),end="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day))
    end_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day),end="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day))
    if start_day_stock_data.empty  :
       #print "当天的数据为空",start_day, "end", end_day
        return
    #大盘指数
    index_sh = ts.get_hist_data('sh',start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))
    if index_sh.empty :
        print "当天大盘数据为空***********************",start_day
        return 
    index_sz = ts.get_hist_data('sz',start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))
    index_cyb = ts.get_hist_data('cyb',start="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day),end="%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day))

    i=1
    while   second_day_stock_data.empty:
        #print "后一天的数据为空 +++++++", second_day
        second_day = datetime.datetime.strptime(trading_days[index+period+i],"%Y%m%d")
        second_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day),end="%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day))
        i +=1

    while   end_day_stock_data.empty:
        #print "后两天的数据为空 +++++++", end_day
        end_day = datetime.datetime.strptime(trading_days[index+period+i],"%Y%m%d")
        end_day_stock_data = ts.get_hist_data(test_stock,start="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day),end="%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day))
        i +=1
    feature = []
    feature.append(start_day_stock_data['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['v_ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['v_ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['v_ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(start_day_stock_data['turnover']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(second_day_stock_data['price_change']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['volume']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['open']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['close']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['high']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['low']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['p_change']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['ma5']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['ma10']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['ma20']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['v_ma5']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['v_ma10']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['v_ma20']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(second_day_stock_data['turnover']["%04d-%02d-%02d" % (second_day.year, second_day.month, second_day.day)])
    feature.append(index_sh['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['v_ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['v_ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sh['v_ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['v_ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['v_ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_sz['v_ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['open']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['high']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['close']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['low']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['volume']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['p_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['price_change']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['ma5']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['ma10']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    feature.append(index_cyb['ma20']["%04d-%02d-%02d" % (start_day.year, start_day.month, start_day.day)])
    label = []
    if end_day_stock_data['price_change']["%04d-%02d-%02d" % (end_day.year, end_day.month, end_day.day)] > 0:
        label.append(0)
        label.append(1)
    else :
        label.append(1)
        label.append(0)
    print "今天日期",start_day
    x_test_all.append(feature)
    y_test_all.append(label)
print "训练数据集----------------------------------------"
for index in range(start_date_index, test_start_index ):
    getXData(index, 1)

print "测试数据集----------------------------------------"

for index in range(test_start_index, end_date_index-2 ):
    getTestData(index, 1)
x = tf.placeholder(tf.float32, [None, 64])
W = tf.Variable(tf.zeros([64,2]))
b = tf.Variable(tf.zeros([2]))

y = tf.nn.softmax(tf.matmul(x,W) + b)
#y_conv是预测的涨跌结果  y_是实际数据
y_ = tf.placeholder("float", [None,2])

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])


x_image = tf.reshape(x, [-1,8,8,1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([2 * 2 * 64, 1024])

b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 2*2*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 2])
b_fc2 = bias_variable([2])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


def chunks(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]

print x_all
x_all_batch = []
y_all_batch = []
x_all_batch = chunks(x_all,100)
y_all_batch = chunks(y_all,100)
init = tf.global_variables_initializer()
sess = tf.InteractiveSession()
sess.run(init)
print "batch -----"
print x_all_batch
print "训练开始了-----"
for i in range(20000):
  j = i % len(x_all_batch)
  if i%100 == 0 :
      train_accuracy = accuracy.eval(feed_dict={x:x_all_batch[j], y_: y_all_batch[j], keep_prob: 1.0})
      print "step %d, training accuracy %g"%(i, train_accuracy)
  train_step.run(feed_dict={x: x_all_batch[j], y_: y_all_batch[j], keep_prob: 0.5})
print "准确率"
print "test accuracy %g"%accuracy.eval(feed_dict={
    x: x_all_batch[1], y_: y_all_batch[1], keep_prob: 1.0})






