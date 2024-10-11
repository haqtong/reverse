import datetime
import holidays

# 创建中国法定节假日的实例（不包含周末）
cn_holidays = holidays.China(years=datetime.datetime.now().year)

# 获取当前日期
today = datetime.datetime.now().date()

# 计算明天（当前日期加一天）
tomorrow = today + datetime.timedelta(days=1)

# 判断明天是否是法定节假日或周末
if tomorrow in cn_holidays:
    print(f"{tomorrow} 是法定节假日，节假日名称: {cn_holidays[tomorrow]}")
elif tomorrow.weekday() >= 5:  # weekday() 返回0（周一）到6（周日）
    print(f"{tomorrow} 是周末（{'周六' if tomorrow.weekday() == 5 else '周日'}）")
else:
    print(f"{tomorrow} 既不是法定节假日也不是周末")