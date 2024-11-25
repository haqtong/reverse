#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   create_data.py    
@Contact :   hqtong@epsoft.com.cn
@Desciption：
------------ 
时间窗口 20230101 - 20241125
------------ 
@Modify Time      @Author    @Version    
------------      -------    --------  
2024/11/25 15:32   hqtong      1.0         
'''

# import lib


#
from config.set_config import *
def get_trait():
    fn = 'reverse_repo.csv'
    infn = os.path.join(Config_base.data_warehouse,fn)
    df = Config_base.read_data(infn)
    # 做7天的滑窗，用于做计算每日流出水平
    df['repo_7'] = df['repo'].shift(7)
    df['trait_x1'] = df.apply(lambda x: x['repo'] - x['repo_7'],axis = 1)
    df = df.dropna(subset=['repo_7'])
    print(df.head())
    return df['trait_x1'].values

def get_label(ts_code = '000002.SH'):
    fn = '000001perf.xlsx'
    infn = os.path.join(Config_base.base_path,'功能测试/相关性检验',fn)
    df = Config_base.read_data(infn)
    df.to_csv('000001_SH.csv')
    print(df.head())


    # data.to_csv('test.csv',index = 0)
    # print(data.columns)
    # print(data)


if __name__ == '__main__':
    get_label()



