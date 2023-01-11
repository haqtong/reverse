#encoding=utf-8
import pandas as pd
import os
from basic_func import basicFunc,warningState,dataWarehouse

def daily_initialize():

    BF = basicFunc()
    # input daily reverse repo
    BF.daily_input()
    DW = dataWarehouse()
    DW.reverse_repo_for_week()
    DW.daily_repo_level()

def daily_broadcast():
    BF = basicFunc()
    # normal broadcast
    BF.broadcast()

if __name__ == '__main__':
    daily_initialize()
    daily_broadcast()

