import numpy as np
import akshare as ak
import pandas as pd
import datetime

sp_elem = ['序号', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '最高', '最低', '今开', '昨收', '量比', '换手率', '市盈率-动态', \
         '市净率', '总市值', '流通市值', '涨速', '五分钟涨跌', '60日涨跌幅', '年初至今涨跌幅']
'''
sp_elem对应序号
0:序号 1:代码 2:名称 3:最新价 4:涨跌幅 5:涨跌额 6:成交量 7:成交额 8:振幅 9:最高 10:最低 11:今开 12:昨收 13:量比 14:换手率 15:市盈率-动态 16:市净率 17:总市值 
18:流通市值 19:涨速 20:五分钟涨跌 21:60日涨跌幅 22:年初至今涨跌幅
'''

hs_elem = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
'''
hs_elem对应序号
0:日期 1:开盘 2:收盘 3:最高 4:最低 5:成交量 6:成交额 7:振幅 8:涨跌幅 9:涨跌额 10:换手率
'''


def separatePrinter():
    print('========================================================================================')
    print('========================================================================================')


def writeAllStockList():
    sp = ak.stock_zh_a_spot_em()
    code_list = sp[[sp_elem[0], sp_elem[1], sp_elem[2], ]].values
    f = open('stockList.txt', 'w')
    for elem in code_list:
        f.write(str(elem) + '\n')
    f.close()

def readStockListAll():
    data = []
    file = open('stockList.txt', 'r')
    file_data = file.readlines()
    for elem in file_data:
        elm = []
        elemAr = elem.split('[')[1].split(']')[0].split(' ')
        elemAr[0] = elemAr[0].replace("'",'')
        elemAr[1] = elemAr[1].replace("'", '')
        elemAr[2] = elemAr[2].replace("'", '')
        elm.append(elemAr[0])
        elm.append(elemAr[1])
        elm.append(elemAr[2])
        data.append(elm)
    return data                      # data[0]:seq  data[1]:cod data[2]:chinese code

def stockDic():
    data = readStockListAll()
    codeList = []
    chineseList = []
    for elem in data:
        codeList.append(elem[1])
        chineseList.append(elem[2])
    dictBase = dict(zip(codeList, chineseList))
    return dictBase


def getDateStr(timeBeforeDays):
    now = str(datetime.date.today())
    daysAgo = str((datetime.date.today() - datetime.timedelta(days=timeBeforeDays)))
    daysAdayAgo = str((datetime.date.today() - datetime.timedelta(days=1)))
    nowStr = now[:4] + now[5:7] + now[8:]
    agoStr = daysAgo[:4] + daysAgo[5:7] + daysAgo[8:]
    daysAdayAgoStr = daysAdayAgo[:4] + daysAdayAgo[5:7] + daysAdayAgo[8:]
    return agoStr, nowStr