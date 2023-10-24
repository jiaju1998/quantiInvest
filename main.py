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

    stg().stg2(20)



    print('end of main func')