# encoding=utf-8
from setting import *
from config import *
import numpy as np
import matplotlib.pyplot as plt
from xlrd import xldate_as_tuple
import datetime

import pandas as pd
import time
import os
def func(data_format):
    # 格式化为时间元组
    timeArray = time.localtime((data_format) * 37026.0)
    # 将时间元组转换为时间字符串
    timeStr = time.strftime('%Y-%m-%d', timeArray)

    return timeStr

def date_cal(stamp):
    delta = pd.Timedelta(str(stamp) + 'D')
    real_time = pd.to_datetime('1899-12-30') + delta
    return real_time

def plot(df):
    x = df['日期'].values
    y = df['逆回购'].values
    y1 = df['七天逆回购总额'].values
    plt.plot(x, y, 'ro-')
    plt.plot(x, y1, 'bo-')
    plt.show()

def exec():
    df = pd.read_excel(data_path, sheet_name='Sheet4')
    df.loc[:, '日期'] = df.apply(lambda x: date_cal(x['日期']), axis=1)
    # 格式化为时间元组
    a = df['逆回购'].values
    short_list = []
    for i in range(df.shape[0]):
        if i == 0:
            indicate = np.sum(a[-7:])
        else:
            indicate = np.sum(a[-7 - i:- i])
        short_list.append(indicate)
    print(indicate)
    short_list.reverse()
    df['七天逆回购总额'] = short_list
    print(short_list)
    plot(df)
    df.to_excel(output_path)
    return df


if __name__ == '__main__':
    exec()
    # data = pd.DataFrame(np.arange(6).reshape((2, 3)),
    #                     index=pd.Index(['Ohio', 'Colorado'], name='state'),
    #                     columns=pd.Index(['one', 'two', 'three'],
    #                                      name='number'))
    # print(data)
    # result = data.stack()
    # print(result)

# version1 绘制近每天近七日数据逆回购值，和单日逆回购水平
# version2 补充同比环比 - 未完成，数量太少不足以支撑
# -*- coding:UTF8 -*-





