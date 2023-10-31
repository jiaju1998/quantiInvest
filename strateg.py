import os
import sys
import numpy as np
from utils import readStockListAll
from utils import getDateStr
from utils import sp_elem, hs_elem, separatePrinter
import akshare as ak
import datetime
from utils import stockDic
import time
from collections import Counter

'''
1:返回最近n天 涨跌幅 前十 glob
2:返回最近n天 成交量 前十 glob
3:返回最近n天 成交量+涨跌幅 前十 glob   线性映射后给权重
'''

class dailyPost:
    def __init__(self):
        self.datetoday = str(datetime.date.today())
        self.datetodaystr = self.datetoday[:4] + self.datetoday[5:7] + self.datetoday[8:]
        self.stockBase = readStockListAll()
        self.stockDic = stockDic()

    def getRate(self):
        sp = ak.stock_zh_a_spot_em()
        code_list = sp[[sp_elem[0], sp_elem[1], sp_elem[2], sp_elem[4], sp_elem[6]]].values
        upStockList = []
        downStockList = []
        stableStockList = []
        turnoverList = []
        for idx in range(len(code_list)):
            count = 0
            curCode = code_list[idx][1]
            curName = code_list[idx][2]
            rateVal = code_list[idx][3]
            turnover = code_list[idx][4]
            tmp_rate = []
            tmp_turnover = []
            tmp_rate.append(curCode)
            tmp_rate.append(curName)
            tmp_rate.append(rateVal)
            tmp_turnover.append(curCode)
            tmp_turnover.append(curName)
            tmp_turnover.append(turnover)
            turnoverList.append(tmp_turnover)
            if rateVal >= 0.0001:
                upStockList.append(tmp_rate)
            elif rateVal <= -0.1:
                downStockList.append(tmp_rate)
            else:
                stableStockList.append(tmp_rate)
        turnoverList.sort(key = lambda ele: ele[2], reverse=True)
        upStockList.sort(key = lambda ele: ele[2], reverse=True)
        downStockList.sort(key = lambda ele: ele[2])
        infoHead = [sp_elem[1], sp_elem[2], sp_elem[4]]
        infoHead_turnover = [sp_elem[1], sp_elem[2], sp_elem[6]]
        upStockList = np.row_stack((infoHead, upStockList))
        downStockList = np.row_stack((infoHead, downStockList))
        turnoverList = np.row_stack((infoHead_turnover, turnoverList))
        return upStockList,downStockList,stableStockList,turnoverList

class stg():
    def __init__(self):
        self.datetoday = str(datetime.date.today())
        self.datetodaystr = self.datetoday[:4] + self.datetoday[5:7] + self.datetoday[8:]
        self.stockBase = readStockListAll()
        self.stockDic = stockDic()

    def timePeriodCheck(self, timeP):
        print('start of time period check')
        dstList = []
        for idx in range(30):                   #统计30只股票在timeP中的开盘日期，选出realTimeP
            curStock = self.stockBase[idx]
            curStockCode = curStock[1]
            curStockName = curStock[2]
            # 一次拿一百天的数据，避免重复访问
            startDate, endDate = getDateStr(timeP)

            flag = 1
            while flag == 1:
                try:
                    hs = ak.stock_zh_a_hist(symbol=curStockCode, start_date=startDate, end_date=endDate)
                    flag = 0
                except:
                    time.sleep(2)

            try:
                targetList = hs[[hs_elem[0], hs_elem[5], hs_elem[8]]].values
            except KeyError:
                print('no info found of this stock!:' + str(curStockCode) + ':' + str(curStockName))
                continue
            dstList.append(len(targetList))
        count = Counter(dstList)
        dst = count.most_common(1)[0][0]
        print('end of time period check')
        print('real time period is: ' + str(dst))
        return dst
    def getRateList(self, list):
        dataPool = []
        for i in range(len(list)):
            dataPool.append(list[i][2])
        maxValue = max(dataPool)
        minValue = min(dataPool)
        #方法1 线性映射
        rankList = list.copy()
        for i in range(len(rankList)):
            tmp = list[i][2]
            mark = 100 * ((tmp - minValue) / (maxValue - minValue))
            rankList[i][2] = mark
        return rankList
    def getTOList(self, list):
        dataPool = []
        for i in range(len(list)):
            dataPool.append(list[i][2])
        maxValue = max(dataPool)
        minValue = min(dataPool)
        #方法1 线性映射
        rankList = list.copy()
        for i in range(len(rankList)):
            tmp = list[i][2]
            mark = 100 * ((tmp - minValue) / (maxValue - minValue))
            rankList[i][2] = mark

        return rankList
    def getFinalMarkList(self, rateMarkList, rateCoe, turnOverMarkList, TOCoe):
        markList = rateMarkList.copy()
        for i in range(len(markList)):
            tmp = rateCoe * rateMarkList[i][2] + TOCoe * turnOverMarkList[i][2]
            markList[i][2] = tmp

        return markList

    def stg1(self, timeP):                   #3天内成交量较为稳定且三天内收益为正的，在后面两天挣钱的概率
        #--------------------------------回测--------------------------------
        numCount = 0
        list_ = []
        for idx in range(len(self.stockBase)):
            curStock = self.stockBase[idx]
            curStockCode = curStock[1]
            curStockName = curStock[2]
            #一次拿一百天的数据，避免重复访问
            startDate, endDate = getDateStr(timeP)

            flag = 1
            while flag == 1:
                try:
                    hs = ak.stock_zh_a_hist(symbol=curStockCode, start_date=startDate, end_date=endDate)
                    flag = 0
                except:
                    time.sleep(2)

            try:
                targetList = hs[[hs_elem[0], hs_elem[5], hs_elem[8]]].values
            except KeyError:
                print('[stg1][test] no info found of this stock!:' + str(curStockCode) + ':' + str(curStockName))
                continue
            totalDays = len(targetList)
            testPeriod = 3                     #3天的测试
            validPeriod = 2                    #2天的验证
            num0 = 0                     #符合策略的num
            num1 = 0                      #符合策略的num中成功上涨的num
            for day in range(totalDays-testPeriod-validPeriod):
                turnover0 = int((targetList[day][1]))
                turnover1 = int(targetList[day + 1][1])
                turnover2 = int(targetList[day + 2][1])
                rate0 = float(targetList[day][2]) + 100
                rate1 = float(targetList[day + 1][2]) + 100
                rate2 = float(targetList[day + 2][2]) + 100
                if (turnover1 >= 0.9 * turnover0) and (turnover2 >= 0.9 * turnover1) and (rate0 * rate1 * rate2 >= 1000000):  #满足条件
                    num0 = num0 + 1
                    rate3 = float(targetList[day + 3][2]) + 100
                    rate4 = float(targetList[day + 4][2]) + 100
                    if rate3 * rate4 >= 10000:  #策略成功
                        num1 = num1 + 1
            tmp_ = []
            tmp_.append(curStockCode)
            tmp_.append(curStockName)
            tmp_.append(num0)
            tmp_.append(num1)
            list_.append(tmp_)
            print("[stg1][test] procNum:" + str(idx) + '    ' + '进入策略的股票数:' + str(num0) + '   进入策略且上涨的股票数:' + str(num1))
            numCount = numCount + 1


        sum0 = 0
        sum1 = 0
        winRateList = []
        # 加入三个list进去，避免winRateList是空list
        winRateList.append(['test0', '00000', 0, 0, 0])
        winRateList.append(['test1', '00000', 0, 0, 0])
        winRateList.append(['test2', '00000', 0, 0 ,0])

        for i in range(len(list_)):
            sum0 = sum0 + list_[i][2]
            sum1 = sum1 + list_[i][3]
            tmp = []
            tmp.append(list_[i][0])
            tmp.append(list_[i][1])
            tmp.append(list_[i][2])
            tmp.append(list_[i][3])
            if list_[i][2] == 0:
                tmp.append(0)
            else:
                tmp.append(list_[i][3] / list_[i][2])
            if list_[i][2] >= 5:
                winRateList.append(tmp)
        winRateList.sort(key=lambda ele: ele[4], reverse=True)
        top20WinRateList = winRateList[0:20]
        # ------------------------------------------------------------------

        # --------------------------------选股--------------------------------
        pickList = []
        pickCount = 0
        startDate, endDate = getDateStr(7)                 #为了避免周末数据不连续，取七天的数据
        for idx in range(len(self.stockBase)):
            pickListElem = []
            curStock = self.stockBase[idx]
            curStockCode = curStock[1]
            curStockName = curStock[2]

            if (2135 == idx):
                debug = 1

            flag = 1
            while flag == 1:
                try:
                    hs = ak.stock_zh_a_hist(symbol=curStockCode, start_date=startDate, end_date=endDate)
                    flag = 0
                except:
                    time.sleep(2)

            try:
                targetList = hs[[hs_elem[0], hs_elem[5], hs_elem[8]]].values
            except KeyError:
                print('[stg1][pick] no info found of this stock!:' + str(curStockCode) + ':' + str(curStockName))
                continue
            targetList = targetList[len(targetList) - 3:]             #取三天的数据
            if len(targetList) != 3:
                continue
            turnover0 = int((targetList[0][1]))
            turnover1 = int(targetList[1][1])
            turnover2 = int(targetList[2][1])
            rate0 = float(targetList[0][2]) + 100
            rate1 = float(targetList[1][2]) + 100
            rate2 = float(targetList[2][2]) + 100
            if (turnover1 >= 0.9 * turnover0) and (turnover2 >= 0.9 * turnover1) and (rate0 * rate1 * rate2 >= 1000000):  # 满足条件
                pickListElem.append(curStockCode)
                pickListElem.append(curStockName)
                pickListElem.append(sum([turnover0,turnover1,turnover2]) / 3)
                pickListElem.append(rate0 * rate1 * rate2)
                pickCount = pickCount + 1
                pickList.append(pickListElem)
            print("[stg1][pick] procNum:" + str(idx))
        pickList.sort(key=lambda ele: ele[2], reverse=True)              #按照成交量排序
        pickListTop20 = pickList[0:20]
        # ------------------------------------------------------------------
        return sum0, sum1, top20WinRateList, numCount, pickListTop20, pickCount


    def stg2(self, timeP):                     # 3天内成交量和涨幅top10的股票，在后面两天挣钱的概率
        # --------------------------------回测--------------------------------
        # 设置系数
        TOCoe = 0.5  # 重要参数，写到接口里去
        rateCoe = 0.5  # 重要参数，写到接口里去
        markThreshold = 80  # 重要参数，写到接口里去

        stockNum = 0
        dashBoard = []
        totalNum = 0                        #进入到策略的总数
        winNum = 0                          #进入到策略且成功上涨的总数
        realTimeP = self.timePeriodCheck(timeP)
        totalList = []
        for idx in range(len(self.stockBase)):
            curStock = self.stockBase[idx]
            curStockCode = curStock[1]
            curStockName = curStock[2]
            #一次拿一百天的数据，避免重复访问
            startDate, endDate = getDateStr(timeP)

            flag = 1
            while flag == 1:
                try:
                    hs = ak.stock_zh_a_hist(symbol=curStockCode, start_date=startDate, end_date=endDate)
                    flag = 0
                except:
                    time.sleep(2)

            try:
                targetList = hs[[hs_elem[0], hs_elem[5], hs_elem[8]]].values
            except KeyError:
                print('[stg2][test] no info found of this stock!:' + str(curStockCode) + ':' + str(curStockName))
                continue

            list0Tmp = []
            if (len(targetList) != realTimeP):
                continue
            for i in range(len(targetList)):
                list1Tmp = []  # [code, name, turnover, rate]
                list1Tmp.append(curStockCode)
                list1Tmp.append(curStockName)
                list1Tmp.append(targetList[i][1])
                list1Tmp.append(targetList[i][2])
                list0Tmp.append(list1Tmp)
            totalList.append(list0Tmp)
            stockNum = stockNum + 1
        testPeriod = 3
        validPeriod = 2
        for day in range(realTimeP - testPeriod - validPeriod):
            turnOverList = []                   #三天的成交量list
            rateList = []                       #三天的涨幅list
            num0 = 0                           #当前day进入策略的股票数
            num1 = 0                           #当前day进入策略且上涨的股票数
            for i in range(len(totalList)):
                tagTmpTO = []
                tagTmpR = []
                tagTmpTO.append(totalList[i][day][0])
                tagTmpTO.append(totalList[i][day][1])
                tagTmpR.append(totalList[i][day][0])
                tagTmpR.append(totalList[i][day][1])
                tagTmpTO.append(totalList[i][day][2] + totalList[i][day + 1][2] + totalList[i][day + 2][2])
                turnOverList.append(tagTmpTO)
                tagTmpR.append((100 + totalList[i][day][3]) * (100 + totalList[i][day + 1][3]) * (100 + totalList[i][day + 2][3]))
                rateList.append(tagTmpR)

            #计算每只股票的分数
            rateMarkList = self.getRateList(rateList)
            turnOverMarkList = self.getTOList(turnOverList)
            markList = self.getFinalMarkList(rateMarkList, rateCoe, turnOverMarkList, TOCoe)
            markList.sort(key=lambda ele: ele[2], reverse=True)
            #把分数高于阈值的股票挑出来
            highMarkList = []
            for i in range(len(markList)):
                if markList[i][2] >= markThreshold:
                    highMarkList.append(markList[i])
                else:
                    break
            num0 = num0 + len(highMarkList)
            #两天的验证
            for i in range(len(highMarkList)):
                curCode = highMarkList[i][0]
                for j in range(len(totalList)):
                    if (totalList[j][day][0] == curCode):
                        twoDaysRate = (totalList[j][day+3][3] + 100) * (totalList[j][day+4][3] + 100)
                        if (twoDaysRate >= 10000):
                            num1 = num1 + 1
                        break
            print("[stg2][test]procDateIdx:" + str(day) + '    ' + '分数阈值：' + str(markThreshold) + '   ' + '进入策略的股票数:' + str(num0) + '   进入策略且上涨的股票数:' + str(num1))
            totalNum = totalNum + num0
            winNum = winNum + num1
        # ------------------------------------------------------------------
        # --------------------------------选股--------------------------------
        pickCount = 0
        totalListPick = []
        for idx in range(len(self.stockBase)):
            curStock = self.stockBase[idx]
            curStockCode = curStock[1]
            curStockName = curStock[2]
            startDate, endDate = getDateStr(10)

            flag = 1
            while flag == 1:
                try:
                    hs = ak.stock_zh_a_hist(symbol=curStockCode, start_date=startDate, end_date=endDate)
                    flag = 0
                except:
                    time.sleep(2)

            try:
                targetList = hs[[hs_elem[0], hs_elem[5], hs_elem[8]]].values
            except KeyError:
                print('[stg2][test] no info found of this stock!:' + str(curStockCode) + ':' + str(curStockName))
                continue

            targetList = targetList[len(targetList) - 3:]                   #取三天的数据
            if (len(targetList) != 3):
                continue
            list0Tmp = []
            for i in range(len(targetList)):
                list1Tmp = []  # [code, name, turnover, rate]
                list1Tmp.append(curStockCode)
                list1Tmp.append(curStockName)
                list1Tmp.append(targetList[i][1])
                list1Tmp.append(targetList[i][2])
                list0Tmp.append(list1Tmp)
            totalListPick.append(list0Tmp)
            print("[stg2][pick] procNum:" + str(idx))
        turnOverList = []  # 三天的成交量list
        rateList = []  # 三天的涨幅list
        num0 = 0  # 当前day进入策略的股票数
        for i in range(len(totalListPick)):
            tagTmpTO = []
            tagTmpR = []
            tagTmpTO.append(totalListPick[i][0][0])
            tagTmpTO.append(totalListPick[i][0][1])
            tagTmpR.append(totalListPick[i][0][0])
            tagTmpR.append(totalListPick[i][0][1])
            tagTmpTO.append(totalListPick[i][0][2] + totalListPick[i][1][2] + totalListPick[i][2][2])
            turnOverList.append(tagTmpTO)
            tagTmpR.append((100 + totalListPick[i][0][3]) * (100 + totalListPick[i][1][3]) * (100 + totalListPick[i][2][3]))
            rateList.append(tagTmpR)
        # 计算每只股票的分数
        rateMarkList = self.getRateList(rateList)
        turnOverMarkList = self.getTOList(turnOverList)
        markList = self.getFinalMarkList(rateMarkList, rateCoe, turnOverMarkList, TOCoe)
        markList.sort(key=lambda ele: ele[2], reverse=True)
        # 把分数高于阈值的股票挑出来
        highMarkList = []
        for i in range(len(markList)):
            if markList[i][2] >= markThreshold:
                highMarkList.append(markList[i])
                pickCount = pickCount + 1
            else:
                break
        #pickList = highMarkList[0:20]
        pickList = markList[0:20]
        # ------------------------------------------------------------------

        return totalNum, winNum, stockNum, TOCoe, rateCoe, markThreshold, pickList, pickCount


