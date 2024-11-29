#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   data_conv.py    
@Contact :   hqtong@epsoft.com.cn
@Desciption：
------------ 

------------ 
@Modify Time      @Author    @Version    
------------      -------    --------  
2024/11/29 16:22   hqtong      1.0         
'''
from config.set_config import *
# import lib
select_col = ['日期Date', '收盘Close']
infn = os.path.join(Config_base.diyprogram_1,'000001perf (1).xlsx')
outfn = os.path.join(Config_base.diyprogram_1,'000001_SH.csv')
ori_df = Config_base.read_data(infn)
ori_df_col = ori_df.columns
print(ori_df_col)
aim_df = pd.DataFrame(ori_df,columns = select_col )
Config_base.dumps_data(aim_df,outfn)

