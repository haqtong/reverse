from datetime import datetime, timedelta

# 定义一组日期
dates = [
    datetime(2021, 1, 1),
datetime(2022, 3, 5),
datetime(2021, 6, 14)
]

# 使用 min() 函数找出最早日期
min_date = min(dates)

print("The earliest date is:", min_date)
