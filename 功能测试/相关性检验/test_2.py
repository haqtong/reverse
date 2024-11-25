import tushare as ts

# 注册后获取的token
token = 'mytoken'
ts.set_token(token)

pro = ts.pro_api()

# 获取大盘指数数据
sh_index = pro.index_daily(ts_code='000001.SH')

print(sh_index)