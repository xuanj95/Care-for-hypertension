import time
import datetime

begin_date = (datetime.datetime.now() - datetime.timedelta(days =15)).strftime("%Y-%m-%d")
date_list = []
begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())), "%Y-%m-%d")
while begin_date <= end_date:
    date_str = begin_date.strftime("%Y-%m-%d")
    date_list.append(date_str)
    begin_date += datetime.timedelta(days=1)
# print(date_list)