# [pytz时区问题](https://github.com/chaleaoch/gitblog/issues/23)

Table of Contents
=================



\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

```
end_datetime = datetime(
                year=now_local_tz.year,
                month=now_local_tz.month,
                day=now_local_tz.day,
                hour=now_local_tz.hour,
                minute=0,
                second=0,
                tzinfo=pytz.timezone(settings.TIME_ZONE)
            )
pytz.timezone(settings.TIME_ZONE)
<DstTzInfo 'Asia/Dubai' LMT+3:41:00 STD>
end_datetime.tzinfo
<DstTzInfo 'Asia/Dubai' LMT+3:41:00 STD>
```
这里的 LMT是指当地时间而不是标准是时区时间.
如何处理?
- 用astimezone
```
end_datetime = datetime(
                year=now_local_tz.year,
                month=now_local_tz.month,
                day=now_local_tz.day,
                hour=now_local_tz.hour,
                minute=0,
                second=0,
            ).astimezone(pytz.timezone(settings.TIME_ZONE))
```
- 标准库dateutil
```
from datetime import timezone as tz
import datetime
from dateutil import tz
cn = tz.gettz('Asia/Shanghai')
 
aware_dt = datetime.datetime(2019,6,20, 12, tzinfo=cn)
print(aware_dt ) # 2019-06-20 12:00:00+08:00
 
# 时区转换(从北京时间转到纽约时间)
ny = tz.gettz('America/New_York')
print(aware_dt.astimezone(tz=ny)) # 2019-06-20 00:00:00-04:00
```