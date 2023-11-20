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
        #stg1 --------------------------------------------
        sum0, sum1, top20WinRateList, numCount, pickListTop20, pickCount = stg().stg1(timePeriod)
        log = addSeperate(log)
        logLine = 'report of stg1'
        log = addLogLine(log, logLine)
        logLine = '回测结果:'
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
        logLine = '选股结果:'
        log = addLogLine(log, logLine)
        logLine = '今日进入策略的股票数： ' + str(pickCount)
        log = addLogLine(log, logLine)
        logLine= 'top20推荐股票:'
        log = addLogLine(log, logLine)
        for elem in pickListTop20:
            logLine = str(elem)
            log = addLogLine(log, logLine)
        log = addSeperate(log)
        log = addSeperate(log)
        # stg2 --------------------------------------------
        totalNum, winNum, stockNum, TOCoe, rateCoe, markThreshold, pickList, pickCount = stg().stg2(timePeriod)
        logLine = 'report of stg2'
        log = addLogLine(log, logLine)
        logLine = 'param--> TOcoeff: ' + str(TOCoe) + '  rateCoeff: ' + str(rateCoe) + '  threshold(max 100): ' + str(markThreshold)
        log = addLogLine(log, logLine)
        logLine = '回测结果:'
        log = addLogLine(log, logLine)
        logLine = '统计的股票数 ' + str(stockNum)
        log = addLogLine(log, logLine)
        logLine = '进入策略次数 ' + str(totalNum)
        log = addLogLine(log, logLine)
        logLine = '进入策略且挣钱次数 ' + str(winNum)
        log = addLogLine(log, logLine)
        logLine = '总成功率：' + str(winNum / totalNum)
        log = addLogLine(log, logLine)
        logLine = '选股结果:'
        log = addLogLine(log, logLine)
        logLine = '入围股票数： ' + str(pickCount)
        log = addLogLine(log, logLine)
        logLine = 'top20推荐股票:'
        log = addLogLine(log, logLine)
        for elem in pickList:
            logLine = str(elem)
            log = addLogLine(log, logLine)
        log = addSeperate(log)
        log = addSeperate(log)
        # stg3 --------------------------------------------
        timeP_stg3, targetDay_stg3, stockCount, factInfo = stg().stg3()
        logLine = 'report of stg3'
        log = addLogLine(log, logLine)
        logLine = '时间周期：' + str(timeP_stg3)
        log = addLogLine(log, logLine)
        logLine = 'targetDay（回测的跑赢周期）：' + str(targetDay_stg3)
        log = addLogLine(log, logLine)
        logLine = '总共统计股票数：' + str(stockCount)
        log = addLogLine(log, logLine)
        for elem in factInfo:
            logLine = '[' + '有效因子： ' + str(elem[6]) + ']'
            log = addLogLine(log, logLine)
            logLine = '相关系数： ' + str(elem[0])
            log = addLogLine(log, logLine)
            logLine = '第一组的平均因子和第五组的平均因子： ' + str(elem[1])
            log = addLogLine(log, logLine)
            logLine = '第一组因子的范围： ' + str(elem[2])
            log = addLogLine(log, logLine)
            logLine = '第五组因子的范围： ' + str(elem[3])
            log = addLogLine(log, logLine)
            logLine = '在targetday后，第一组因子下跑赢的概率和第五组因子下跑赢的概率： ' + str(elem[4])
            log = addLogLine(log, logLine)
            logLine = '在targetday后，第一组和第五组因子下盈利中位数（单位%）： ' + str(elem[5])
            log = addLogLine(log, logLine)
        log = addSeperate(log)
        log = addSeperate(log)

        with open(logFilePath, "w", encoding="utf-8") as file:
            file.write(log)




    print('end of main func')

#end of main
