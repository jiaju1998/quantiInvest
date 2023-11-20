import numpy as np
import akshare as ak
import pandas as pd
import datetime
from utils import stockDic
from utils import readStockListAll
from utils import getDateStr
from utils import hs_indic_elem, hs_elem
import math
import statistics


def nancheck(srclist):
    new_list = [x for x in srclist if not math.isnan(x)]
    return new_list


def getMultFactorList(dataGround, realTimeP, factorIdx):
    factorName = ['市盈率','市盈率ttm','市净率','市销率','市销率ttm','股息率','股息率ttm','总市值','成交量', '成交额','振幅','换手率','换手率变动']
    timePList = []
    for idx_day in range(realTimeP):
        dailyList = []
        for idx_stock in range(len(dataGround)):
            tmpList = []
            tmpList.append(dataGround[idx_stock][factorIdx][idx_day])  # factor0
            tmpList.append(dataGround[idx_stock][13][idx_day])  # rate
            if np.isnan(tmpList[0]) != 1:
                dailyList.append(tmpList)
        timePList.append(dailyList)
    # 下一步：求31天相关性的均值
    coeffAvgList = []
    FactGroup0Avg = []
    FactGroup4Avg = []
    group0FactorRange = [1000000000000000000, -1000000000000000000]
    group4FactorRange = [1000000000000000000, -1000000000000000000]
    group0info = [0, 0]
    group4info = [0, 0]
    group0rate = []
    group4rate = []
    for day_idx in range(len(timePList)):
        tmpList = timePList[day_idx]
        tmpList.sort(key=lambda ele: ele[0], reverse=False)
        listFact, listRate = [], []
        for elem in tmpList:
            listFact.append(elem[0])
            listRate.append(elem[1])
        data = {'factorX': listFact, 'Rate': listRate}
        df = pd.DataFrame(data)
        corrCoeff = df.corr()['Rate'].values[0]
        coeffAvgList.append(corrCoeff)
        #将数据分为5组
        amountPerGroup = math.floor(len(listFact) / 5)
        delta = len(listFact) % 5
        #group1FactorRange, group5FactorRange = [listFact[0],listFact[amountPerGroup - 1]], [listFact[len(listFact) - (amountPerGroup + delta)], listFact[len(listFact) - 1]]
        if listFact[0] <= group0FactorRange[0]:
            group0FactorRange[0] = listFact[0]
        if listFact[amountPerGroup - 1] >= group0FactorRange[1]:
            group0FactorRange[1] = listFact[amountPerGroup - 1]
        if listFact[len(listFact) - (amountPerGroup + delta)] <= group4FactorRange[0]:
            group4FactorRange[0] = listFact[len(listFact) - (amountPerGroup + delta)]
        if listFact[len(listFact) - 1] >= group4FactorRange[1]:
            group4FactorRange[1] = listFact[len(listFact) - 1]
        sumGroup0 = 0
        sumGroup4 = 0
        factGroup0 = listFact[:amountPerGroup]
        factGroup4 = listFact[len(listFact) - (amountPerGroup + delta):]
        rateGroup0 = listRate[:amountPerGroup]
        rateGroup4 = listRate[len(listFact) - (amountPerGroup + delta):]
        group0RateMedian = statistics.median(rateGroup0)
        group4RateMedian = statistics.median(rateGroup4)
        group0rate.append(group0RateMedian)
        group4rate.append(group4RateMedian)
        FactGroup0Avg.append(sum(factGroup0) / len(factGroup0))
        FactGroup4Avg.append(sum(factGroup4) / len(factGroup4))
        sum0 = 0       #统计goup0上涨概率
        for i in range(amountPerGroup):
            if listRate[i] > 0:
                sum0 = sum0 + 1
        group0info[0] = group0info[0] + sum0
        group0info[1] = group0info[1] + amountPerGroup
        sum0 = 0
        for i in range((len(listFact) - (amountPerGroup + delta)), len(listFact)):
            if listRate[i] > 0:
                sum0 = sum0 + 1
        group4info[0] = group4info[0] + sum0
        group4info[1] = group4info[1] + amountPerGroup + delta

    coeffAvgList = nancheck(coeffAvgList)
    FactGroup0Avg = nancheck(FactGroup0Avg)
    FactGroup4Avg = nancheck(FactGroup4Avg)
    group0rate = nancheck(group0rate)
    group4rate = nancheck(group4rate)
    coeffAvg = sum(coeffAvgList) / len(coeffAvgList)
    fact0AVG = sum(FactGroup0Avg) / len(FactGroup0Avg)
    fact4AVG = sum(FactGroup4Avg) / len(FactGroup4Avg)
    group0RateMidd = statistics.median(group0rate)
    group4RateMidd = statistics.median(group4rate)
    group0Winchance = group0info[0] / group0info[1]
    group4Winchance = group4info[0] / group4info[1]

    frame = []
    frame.append(coeffAvg)
    frame.append([fact0AVG, fact4AVG])
    frame.append(group0FactorRange)
    frame.append(group4FactorRange)
    frame.append([group0Winchance, group4Winchance])
    frame.append([group0RateMidd, group4RateMidd])
    frame.append(factorName[factorIdx])

    return frame
'''
注：因子递增排列，即第一组因子最小，第五组最大
coeffAvg：平均相关系数，可正可负
[fact0AVG, fact4AVG]：第一组的平均因子和第五组的平均因子
group0FactorRange：第一组因子的范围
group4FactorRange：第五组因子的范围
[group0Winchance, group4Winchance]：在targetday后，第一组因子下跑赢的概率和第五组因子下跑赢的概率
[group0RateMidd, group4RateMidd]：在targetday后，第一组和第五组因子下盈利中位数（单位%）
'''

