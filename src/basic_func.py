# encoding = 'utf-8'
import pandas as pd
import datetime
from datetime import date, timedelta
import numpy as np
import math
import os
from config.set_config import Config_base


class basicFunc():
    def __init__(self):
        pass

    def date_cal(self, stamp):
        delta = pd.Timedelta(str(stamp) + 'D')
        real_time = pd.to_datetime('1899-12-30') + delta
        return real_time

    def reverse_repo(self):
        path = r'data\中国人民银行.xlsx'
        df = pd.read_excel(path, sheet_name='Sheet4')
        df = pd.DataFrame(df, columns=['日期', '逆回购'])
        df = df.rename(columns={'日期': 'day_stap', '逆回购': 'reverse_repo_value'})
        df.loc[:, 'day_stap'] = df['day_stap'].apply(lambda x: self.date_cal(x))
        df.loc[:, 'time_stap'] = df['day_stap'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        df.to_csv('data/reverse_repo.csv')

    def daily_input(self):
        path = r'data\reverse_repo.csv'
        record_list = pd.read_csv(path)
        WS = warningState()
        record_list = WS.continuity(record_list)
        record_list.to_csv(path, index=0)

        now = datetime.datetime.now()
        day = now.strftime("%Y-%m-%d")
        time_stap = now.strftime("%Y-%m-%d %H:%M:%S")
        print('请输入当天的逆回购水平：')
        repo = input()
        daily_record = pd.DataFrame([day, repo, time_stap]).T
        daily_record.to_csv(path, mode='a', header=False, index=0)
        record_list = pd.read_csv(path)
        print(record_list.head())

        record = self.daily_data_check(record_list)
        record.to_csv(path)

    def annual_input(self):
        path = r'data\reverse_annual_repo.csv'
        now = datetime.datetime.now()
        day = now.strftime("%Y-%m-%d")
        time_stap = now.strftime("%Y/%m/%d %H:%M:%S")
        print('请输入当天的年度逆回购水平：')
        repo = input()
        daily_record = pd.DataFrame([day, repo, time_stap]).T
        daily_record.to_csv(path, mode='a', header=False, index=0)
        record_list = pd.read_csv(path)
        record = self.daily_data_check(record_list)
        record.to_csv(path, index=0)

    def double_weekly_input(self):
        path = r'data\reverse_double_weekly_repo.csv'
        now = datetime.datetime.now()
        day = now.strftime("%Y-%m-%d")
        time_stap = now.strftime("%Y/%m/%d %H:%M:%S")
        print('请输入当天的14天逆回购水平：')
        repo = input()
        daily_record = pd.DataFrame([day, repo, time_stap]).T
        daily_record.to_csv(path, mode='a', header=False, index=0)
        record_list = pd.read_csv(path)
        print(record_list.head())
        record = self.daily_data_check(record_list)
        record.to_csv(path, index=0)

    def daily_data_check(self, record):  # - >record - df
        record.columns = ['day_stap', 'repo', 'time_stap']
        record = record.copy()
        record.loc[:, 'rank'] = record.groupby('day_stap')['time_stap'].rank('first', ascending=False)
        record = record[record['rank'] == 1].copy()
        record = pd.DataFrame(record, columns=['day_stap', 'repo', 'time_stap'])

        return record

    def timestap_cal(self, date_stap, type='year'):
        print(date_stap)
        date_stap = datetime.datetime.strptime(date_stap, '%Y-%m-%d')

        aim_dict = {'daily': 1, 'weekly': 14}
        if type in list(aim_dict.keys()):
            future_date = date_stap + timedelta(days=aim_dict[type])
        else:
            # conv yyyy mm dd str 格式
            conv_year = date_stap.year + 1
            future_date = datetime.datetime(conv_year, date_stap.month, date_stap.day)
        return future_date

    def valid_gap(self, date_stap, type='year'):
        # print(date_stap)
        date_stap = datetime.datetime.strptime(date_stap, '%Y-%m-%d')
        # print(date_stap)
        base_time = datetime.datetime.now()
        aim_dict = {'daily': 7, 'weekly': 14}
        if type in list(aim_dict.keys()):
            future_date = date_stap + timedelta(days=aim_dict[type])
        else:
            # conv yyyy mm dd str 格式
            # print(date_stap)
            # print(date_stap.month)
            conv_year = date_stap.year + 1
            # print(conv_year)
            try:
                future_date = datetime.datetime(conv_year, date_stap.month, date_stap.day)
            except:
                future_date = datetime.datetime(conv_year, date_stap.month - 1, date_stap.day)  # 平年2月没有29号
            # print(future_date)
        # print(base_time)
        if future_date >= base_time:
            return 'valid'
        else:
            return 'invalid'

    def get_cash_flow(self):
        time_annually = Config_base.read_data(os.path.join(Config_base.data_warehouse, 'reverse_annual_repo.csv'))
        time_weekly = Config_base.read_data(os.path.join(Config_base.data_warehouse, 'reverse_double_weekly_repo.csv'))
        time_daily = Config_base.read_data(os.path.join(Config_base.data_warehouse, 'reverse_repo.csv'))
        time_daily.loc[:, 'state'] = time_daily['day_stap'].apply(lambda x: self.valid_gap(x, 'daily'))
        time_weekly.loc[:, 'state'] = time_weekly['day_stap'].apply(lambda x: self.valid_gap(x, 'weekly'))
        time_annually.loc[:, 'state'] = time_annually['day_stap'].apply(lambda x: self.valid_gap(x))
        print(time_annually.tail())
        daily_cash_flow_dict = time_daily[time_daily['state'] == 'valid'].set_index('day_stap')['repo'].to_dict()
        weekly_cash_flow_dict = time_weekly[time_weekly['state'] == 'valid'].set_index('day_stap')['repo'].to_dict()
        annually_cash_flow_dict = time_annually[time_annually['state'] == 'valid'].set_index('day_stap')['repo'].to_dict()
        print(annually_cash_flow_dict)

        # print(list(daily_cash_flow_dict.values()))
        daily_cash_flow = np.sum(list(daily_cash_flow_dict.values()))
        weekly_cash_flow = np.sum(list(weekly_cash_flow_dict.values()))
        annually_cash_flow = np.sum(list(annually_cash_flow_dict.values()))
        conv_stap_daily, near_expired_cash_daily, conv_stap_monthly, near_expired_cash_monthly, conv_stap_annually, near_expired_cash_annually = 0, 0, 0, 0, 0, 0
        if daily_cash_flow > 0:
            time_stap_daily = min([x for x in list(daily_cash_flow_dict.keys())])
            conv_stap_daily = self.timestap_cal(time_stap_daily, type='daily')
            near_expired_cash_daily = daily_cash_flow_dict[time_stap_daily]
        if weekly_cash_flow > 0:  # 取最小
            time_stap_mothly = min([x for x in list(weekly_cash_flow_dict.keys())])
            conv_stap_monthly = self.timestap_cal(time_stap_mothly, type='weekly')
            near_expired_cash_monthly = weekly_cash_flow_dict[time_stap_mothly]
        if annually_cash_flow > 0:
            time_stap_annually = min([x for x in list(annually_cash_flow_dict.keys())])
            conv_stap_annually = self.timestap_cal(time_stap_annually)
            near_expired_cash_annually = annually_cash_flow_dict[time_stap_annually]
        total_cash = daily_cash_flow + weekly_cash_flow + annually_cash_flow

        return total_cash, annually_cash_flow, conv_stap_annually, near_expired_cash_annually, weekly_cash_flow, conv_stap_monthly, near_expired_cash_monthly, daily_cash_flow, near_expired_cash_daily

    def broadcast(self):
        double_weekly_df = pd.read_csv(r'data\reverse_double_weekly_repo.csv')
        annual_df = pd.read_csv(r'data\reverse_annual_repo.csv')
        daily_net_outflow_df = pd.read_csv(r'output\daily_net_outflow.csv')
        reverse_repo_for_week_df = pd.read_csv(r'output\reverse_repo_for_week.csv')
        today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        daily_net_outflow_df = daily_net_outflow_df[daily_net_outflow_df['day_stap'] == today].copy()
        reverse_repo_for_week_df = reverse_repo_for_week_df[reverse_repo_for_week_df['day_stap'] == today].copy()
        repo_daily = daily_net_outflow_df['repo'].values[0]
        outflow_daily = daily_net_outflow_df['outflow'].values[0]
        repo_for_week = reverse_repo_for_week_df['repo_for_week'].values[0]
        try:
            week_val = int(double_weekly_df[double_weekly_df['day_stap'] == today]['repo'].values[0])
        except:
            week_val = 0
        try:
            annual_val = int(annual_df[annual_df['day_stap'] == today]['repo'].values[0])
        except:
            annual_val = 0

        total_cash, annually_cash_flow, conv_stap_annually, near_expired_cash_annually, weekly_cash_flow, conv_stap_monthly, near_expired_cash_monthly, daily_cash_flow, near_expired_cash_daily = self.get_cash_flow()
        # if bool:
        print(
            '逆回购池共计{}亿，其中\n年度逆回购留存{}亿，最近将于{}到期{}亿；\n14天逆回购留存{}亿，最近将于{}到期{}亿；\n7天逆回购留存{},明日将到期{}亿；'.format(total_cash,
                                                                                                annually_cash_flow,
                                                                                                conv_stap_annually,
                                                                                                near_expired_cash_annually,
                                                                                                weekly_cash_flow,
                                                                                                conv_stap_monthly,
                                                                                                near_expired_cash_monthly,
                                                                                                daily_cash_flow,
                                                                                                near_expired_cash_daily))
        if outflow_daily > 0:
            print('央行7天逆回购{}亿,7天期限累计{}亿；单日逆回购净流入{}亿'.format(repo_daily, repo_for_week, math.fabs(outflow_daily)))
        elif outflow_daily < 0:
            print('央行7天逆回购{}亿,7天期限累计{}亿；单日逆回购净流出{}亿'.format(repo_daily, repo_for_week, math.fabs(outflow_daily)))
        else:
            print('央行7天逆回购{}亿,7天期限累计{}亿；单日逆回购持平'.format(repo_daily, repo_for_week))
        if week_val > 0:
            print('央行14天逆回购{}亿'.format(week_val))
        if annual_val > 0:
            print('央行年度逆回购{}亿'.format(annual_val))


class warningState:
    def __init__(self):
        pass

    def continuity(self, repo_df):

        sdate = date(2023, 1, 28)  # start date
        edate = datetime.datetime.now()
        date_list = pd.date_range(sdate, edate - timedelta(days=1), freq='d')
        std_df = pd.DataFrame(date_list, columns=['day_stap'])
        std_df = std_df.copy()
        std_df.loc[:, 'day_stap'] = std_df['day_stap'].apply(lambda x: x.strftime("%Y-%m-%d"))
        try:
            repo_df.loc[:, 'day_stap'] = repo_df['day_stap'].apply(
                lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime("%Y-%m-%d"))
        except:
            repo_df.loc[:, 'day_stap'] = repo_df['day_stap'].apply(
                lambda x: datetime.datetime.strptime(x, '%Y/%m/%d').strftime("%Y-%m-%d"))
        check_df = std_df.merge(repo_df, on='day_stap', how='left')
        check_df.loc[:, 'day_stap_date'] = pd.to_datetime(check_df['day_stap'], format='%Y-%m-%d')
        check_df.loc[:, 'tag'] = check_df['day_stap_date'].apply(lambda x: 'workday' if x.weekday() < 5 else 'weekend')
        error_cnt = check_df[check_df['repo'].isnull()].shape[0]
        if error_cnt > 0:
            print('存在丢失数据')
            # print(check_df)
            check_df.loc[(check_df['tag'] == 'weekend') & check_df['repo'].isnull(), 'repo'] = 0
            check_df.loc[(check_df['tag'] == 'weekend') & check_df['time_stap'].isnull(), 'time_stap'] = check_df[
                'day_stap_date'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
            print('完成修正')
            # print(check_df)
            error_cnt = check_df[check_df['repo'].isnull()].shape[0]
            if error_cnt > 0:
                print('存在丢失数据需要手动补充，时间为：')
                print(check_df.columns)
                missing_date = check_df[check_df['repo'].isnull()]['day_stap'].values.tolist()
                print(missing_date)
        else:
            print('完成数据检查，数据合格')
        check_df = pd.DataFrame(check_df, columns=['day_stap', 'repo', 'time_stap'])
        return check_df


class dataWarehouse:
    def __init__(self):
        pass

    def reverse_repo_for_week(self):
        path = r'data\reverse_repo.csv'
        df = pd.read_csv(path, encoding='gbk')
        repo_list = df['repo'].values.tolist()
        day_stap_list = df['day_stap'].values.tolist()
        repo_cnt = len(repo_list)
        reverse_repo_for_week = []
        valid_section_list = []
        for i in range(repo_cnt):
            aim_section = repo_list[:i + 1]
            valid_section = aim_section
            valid_section_list.append(valid_section[-7:])
            reverse_repo_for_week.append(np.sum(valid_section[-7:]))
        reverse_repo_for_week_df = pd.DataFrame([day_stap_list, valid_section_list, reverse_repo_for_week]).T
        reverse_repo_for_week_df.columns = ['day_stap', 'valid_section', 'repo_for_week']
        reverse_repo_for_week_df.to_csv('output/reverse_repo_for_week.csv')
        return reverse_repo_for_week_df

    def daily_repo_level(self):
        path = r'data\reverse_repo.csv'
        df = pd.read_csv(path, encoding='gbk')
        day_stap_list = df['day_stap'].values.tolist()
        repo_list = df['repo'].values.tolist()
        repo_cnt = len(repo_list)
        prior_repo = []
        for i in range(repo_cnt):
            aim_section = repo_list[:i + 1]
            # for ele in aim_section:
            #     if ele != 0:
            #         valid_section.append(ele)
            valid_section = aim_section
            if len(valid_section) >= 8:
                prior_repo.append(valid_section[-8])
            else:
                prior_repo.append(0)
        daily_net_outflow_df = pd.DataFrame([day_stap_list, repo_list, prior_repo]).T
        daily_net_outflow_df.columns = ['day_stap', 'repo', 'prior_repo']
        daily_net_outflow_df.loc[:, 'outflow'] = daily_net_outflow_df.apply(lambda x: x['repo'] - x['prior_repo'],
                                                                            axis=1)
        daily_net_outflow_df.to_csv('output/daily_net_outflow.csv', index=0)

    def double_weekly_repo_level(self):
        path = r'data\reverse_repo.csv'
        df = pd.read_csv(path, encoding='gbk')
        day_stap_list = df['day_stap'].values.tolist()
        repo_list = df['repo'].values.tolist()
        repo_cnt = len(repo_list)
        prior_repo = []
        for i in range(repo_cnt):
            aim_section = repo_list[:i + 1]
            # for ele in aim_section:
            #     if ele != 0:
            #         valid_section.append(ele)
            valid_section = aim_section
            if len(valid_section) >= 15:
                prior_repo.append(valid_section[-15])
            else:
                prior_repo.append(0)
        daily_net_outflow_df = pd.DataFrame([day_stap_list, repo_list, prior_repo]).T
        daily_net_outflow_df.columns = ['day_stap', 'repo', 'prior_repo']
        daily_net_outflow_df.loc[:, 'outflow'] = daily_net_outflow_df.apply(lambda x: x['repo'] - x['prior_repo'],
                                                                            axis=1)
        daily_net_outflow_df.to_csv('output/daily_net_outflow.csv', index=0)

    def annual_weekly_repo_level(self):
        pass


if __name__ == '__main__':
    bf = basicFunc()
    bf.broadcast()
    # DW = dataWarehouse()
    # DW.reverse_repo_for_week()
    # DW.daily_repo_level()
