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
    if (stgIdx == '1'):
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


    elif (stgIdx == '2'):
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


    print('end of main func')
