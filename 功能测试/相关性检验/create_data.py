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
    df.loc[:,'日期Date'] = df['day_stap'].apply(lambda x: x.replace('-',''))
    print(df.head(1))
    df['日期Date'] =  df['日期Date'].astype('str')
    df.to_csv('repo_7_test.csv')

    print(df.columns)

    return df

def get_label(ts_code = '000002.SH'):
    fn = '000001_SH.csv'
    infn = os.path.join(Config_base.base_path,'功能测试/相关性检验',fn)
    ori_df = Config_base.read_data(infn)
    print(ori_df.columns)
    select_col = ['日期Date','收盘Close']
    df = pd.DataFrame(ori_df,columns=select_col)
    df['日期Date'] =  df['日期Date'].astype('str')
    print(df.columns)
    df['收盘Close_1'] = df['收盘Close'].shift(1)
    # df = df.dropna(subset = ['收盘Close_1'])
    df['wave'] = df.apply(lambda x: round(x['收盘Close']/x['收盘Close_1']-1,4),axis = 1)

    return df


if __name__ == '__main__':
    df_1 = get_label()
    df_2 = get_trait()
    aim_df = df_2.merge(df_1,on = '日期Date',how = 'left')
    aim_df = aim_df.dropna()
    # aim_df = pd.DataFrame(aim_df,columns = ['日期Date','repo_7',''])
    aim_df = pd.DataFrame(aim_df,columns = ['日期Date','trait_x1','收盘Close','收盘Close_1','wave'])
    aim_df.to_csv('basic_data.csv')

    # print()


