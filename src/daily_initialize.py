#encoding=utf-8
import pandas as pd
import os
from src.basic_func import basicFunc,warningState,dataWarehouse

BF = basicFunc()
def daily_initialize():
    '''

    :return:
    '''

    # input daily reverse repo
    BF.daily_input()
    DW = dataWarehouse()
    DW.reverse_repo_for_week()
    DW.daily_repo_level()

def daily_broadcast():
    BF.broadcast()

def annual_initialize():
    # input annual reverse repo
    BF.annual_input()
    # DW = dataWarehouse()
    # DW.reverse_repo_for_week()
    # DW.daily_repo_level()

def double_weekly_initialize():
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
def exec():
    daily_initialize()
    # annual_initialize()
    # double_weekly_initialize()
    daily_broadcast()
    # pass

if __name__ == '__main__':
    exec()


