#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py    
@Contact :   hqtong@epsoft.com.cn
@Desciption：
------------ 
检验逆回购和大盘波动的相关性
------------ 
@Modify Time      @Author    @Version    
------------      -------    --------  
2024/11/25 14:47   hqtong      1.0         
'''
# import lib
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import statsmodels.api as sm

# 生成示例数据
np.random.seed(0)
n = 100
x = np.random.randn(n).cumsum()  # 生成一个随机的时间序列数据
y = 0.5 * x + np.random.randn(n)  # y 是 x 的线性函数加上一些噪声

# 将数据放入DataFrame中
data = pd.DataFrame({'x': x, 'y': y})

# 检验两个变量的相关性（使用皮尔逊相关系数）
correlation, _ = pearsonr(data['x'], data['y'])
print(f'皮尔逊相关系数: {correlation:.2f}')

# 创建一个新的列来存储x的滞后值（t-1）
data['x_lag1'] = data['x'].shift(1)

# 删除第一行，因为滞后值在第一行是NaN
data = data.dropna()

# 使用简单线性回归模型（OLS）来预测x基于x_lag1
X = data[['x_lag1']]
y_target = data['x']

model = sm.OLS(y_target, X).fit()
print(model.summary())

# 使用模型进行预测（这里只是为了演示，实际上会预测训练集本身）
predictions = model.predict(X)

# 打印预测值和实际值的对比
print(data[['x', 'x_lag1', 'predictions']].head())

# 如果你想预测未来的值，你需要提供未来的x_lag1值。例如，假设我们知道最后一个x_lag1是data中的最后一个值：
last_x_lag1 = data['x_lag1'].iloc[-1]
future_prediction = model.predict(pd.DataFrame({'x_lag1': [last_x_lag1]}))
print(f'对未来一个时间点的预测: {future_prediction.iloc[0]:.2f}')
