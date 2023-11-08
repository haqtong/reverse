#encoding=utf-8
import pandas as pd
import os
from basic_func import basicFunc,warningState,dataWarehouse

def daily_initialize():
    '''

    :return:
    '''

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

def annual_initialize():
    BF = basicFunc()
    # input annual reverse repo
    BF.annual_input()
    # DW = dataWarehouse()
    # DW.reverse_repo_for_week()
    # DW.daily_repo_level()

def double_weekly_initialize():
    BF = basicFunc()
    # input annual reverse repo
    BF.double_weekly_input()
    # DW = dataWarehouse()
    # DW.reverse_repo_for_week()
    # DW.daily_repo_level()

def plotshow():
    # infn = r'D:\program\data\reverse\src\data\reverse_repo.csv'
    # df = pd.read_csv(infn)
    # df.loc[:,'月份'] = df['day_stap'].apply(lambda x:)
    # print(df.head())
    # plotshow()
    pass # 好像tableau更方便

if __name__ == '__main__':
    daily_initialize()
    # annual_initialize()
    # double_weekly_initialize()
    daily_broadcast()


