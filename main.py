import os
import sys
import numpy as np
import akshare as ak
import pandas as pd
from utils import sp_elem, hs_elem, separatePrinter, getDateStr
# from pushPlus import msgSend
from strateg import stg
import schedule
import time
import datetime
from logPrinter import addSeperate
from logPrinter import addLogLine

# def runMyProc():
#     msgSend().do()
#
# schedule.every(1).day.do(runMyProc)
#
# if __name__ == '__main__':
#     msgSend().do()
#     while True:
#         schedule.run_pending
if __name__ == '__main__':
    print('start of main func!')
    stgIdx = sys.argv[1]
    timePeriod = int(sys.argv[2])

    mod = 0                  # 0：验证每个策略每天的数据     1：命令行选择策略验证
    if mod == 1:
        if stgIdx == '1':
            sum0, sum1, top20WinRateList, numCount = stg().stg1(timePeriod)
            print('--------------------------------------------------------------------------------')
            print('report of stg1')
            print('统计的股票数 ' + str(numCount))
            print('回测周期（天） ' + str(timePeriod))
            print('进入策略次数 ' + str(sum0))
            print('进入策略且挣钱次数 ' + str(sum1))
            print('总成功率：' + str(sum1 / sum0))
            print('top 20 stocks:')
            for elem in top20WinRateList:
                print(elem)
            print('--------------------------------------------------------------------------------')


        elif stgIdx == '2':
            totalNum, winNum, stockNum = stg().stg2(timePeriod)
            print('--------------------------------------------------------------------------------')
            print('report of stg2')
            print('统计的股票数 ' + str(stockNum))
            print('进入策略次数 ' + str(totalNum))
            print('进入策略且挣钱次数 ' + str(winNum))
            print('总成功率：' + str(winNum / totalNum))
            print('--------------------------------------------------------------------------------')

        else:
            print('no strategy support')
    elif mod == 0:
        log = ''
        logFileName = str(datetime.date.today()) + '.txt'
        logFilePath = 'dailyReport/' + logFileName
        sum0, sum1, top20WinRateList, numCount = stg().stg1(timePeriod)
        log = addSeperate(log)
        #stg1
        logLine = 'report of stg1'
        log = addLogLine(log, logLine)
        logLine = '统计的股票数 ' + str(numCount)
        log = addLogLine(log, logLine)
        logLine = '回测周期（天） ' + str(timePeriod)
        log = addLogLine(log, logLine)
        logLine = '进入策略次数 ' + str(sum0)
        log = addLogLine(log, logLine)
        logLine = '进入策略且挣钱次数 ' + str(sum1)
        log = addLogLine(log, logLine)
        logLine = '总成功率：' + str(sum1 / sum0)
        log = addLogLine(log, logLine)
        logLine = 'top 20 stocks:'
        log = addLogLine(log, logLine)
        for elem in top20WinRateList:
            logLine = str(elem)
            log = addLogLine(log, logLine)
        log = addSeperate(log)
        log = addSeperate(log)
        # stg2
        totalNum, winNum, stockNum, TOCoe, rateCoe, markThreshold = stg().stg2(timePeriod)
        logLine = 'report of stg2'
        logLine = 'param--> TOcoeff: ' + str(TOCoe) + '  rateCoeff: ' + str(rateCoe) + '  threshold(max 100): ' + str(markThreshold)
        log = addLogLine(log, logLine)
        logLine = '统计的股票数 ' + str(stockNum)
        log = addLogLine(log, logLine)
        logLine = '进入策略次数 ' + str(totalNum)
        log = addLogLine(log, logLine)
        logLine = '进入策略且挣钱次数 ' + str(winNum)
        log = addLogLine(log, logLine)
        logLine = '总成功率：' + str(winNum / totalNum)
        log = addLogLine(log, logLine)
        log = addSeperate(log)

        with open(logFilePath, "w", encoding="utf-8") as file:
            file.write(log)


    print('end of main func')



