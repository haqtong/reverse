# encoding=utf-8
import logging
import pandas as pd
import numpy as np
import datetime
from datetime import date, timedelta
import os
import sys
import json
import math

np.random.seed(913)
fn = sys.argv[0].split('/')[-1].split('.')[0]
filename = 'log/' + sys.argv[0].split('/')[-1].split('.')[0] + '.log'




def ini_reverse_double_weekly_repo():
    sdate = date(2023, 1, 28)  # start date
    edate = date(2023, 9, 22)  # end date
    outfn = r'data\reverse_double_weekly_repo.csv'
    # edate = datetime.datetime.now()
    date_list = pd.date_range(sdate, edate - timedelta(days=1), freq='d')
    std_df = pd.DataFrame(date_list, columns=['day_stap'])
    std_df.loc[:, 'time_stap'] = std_df['day_stap'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    std_df.loc[:, 'day_stap'] = std_df['day_stap'].apply(lambda x: x.strftime("%Y-%m-%d"))
    std_df['repo'] = 0
    std_df = pd.DataFrame(std_df,columns=['day_stap','repo','time_stap'])
    std_df.to_csv(outfn,index = 0)

def exec():
    ini_reverse_double_weekly_repo()

if __name__ == '__main__':
    exec()