# [APScheduler源码小剖](https://github.com/chaleaoch/gitblog/issues/47)


Table of Contents
=================



\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
APScheduler是一个基于python的定时任务,设计很小巧. 源码很易读. 而且里面可以选择gevent/asyncio/twisted等等io组件.和mongodb/redis/zookeeper等存储组件. 所以阅读aps的源码除了有利于理解这个定时任务库之外, 也可以作为client端更进一步理解io组件和存储组件的使用.

aps的源码结构很简单, 实际上aps的组成也是由这几部分组成

- executor -- 执行job的组件, 线程/进程/gevent等

- jobstores -- job的持久化, 存储job的next_run_time等信息

- schedulers -- 调度器,核心.

- triggers -- 时间控制器, 获取下次运行时间什么的都是这个组件做的.

- job - 独立的执行单元, task绑定到它身上.

![](https://tcs.teambition.net/storage/3121d4383b42ccc33fe64fbc3e02f590f739?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IjVlMDBiM2QzNzBiNTNhMDAwMWJhNmJkYyIsImV4cCI6MTYxMjA4MzY4OSwiaWF0IjoxNjExNDc4ODg5LCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzMxMjFkNDM4M2I0MmNjYzMzZmU2NGZiYzNlMDJmNTkwZjczOSJ9.0idhKB3bQfJlIgQAnOuU9DBaTgcwUyEx1Nn_ZE0mgfA&download=image.png "")

下图左边是组件介绍,右边是死循环的大致流程.

![](https://tcs.teambition.net/storage/31211319ec5014e2c155671dd912fb312864?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IjVlMDBiM2QzNzBiNTNhMDAwMWJhNmJkYyIsImV4cCI6MTYxMjA4NDI0NCwiaWF0IjoxNjExNDc5NDQ0LCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzMxMjExMzE5ZWM1MDE0ZTJjMTU1NjcxZGQ5MTJmYjMxMjg2NCJ9.iyqJOj0AlxVNZ2iYZro2_hUcJgl3Vl7TcS0skR_Towk&download=apscheduler.png "")

