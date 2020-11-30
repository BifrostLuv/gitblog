# [rabbitmq笔记](https://github.com/chaleaoch/gitblog/issues/30)

Table of Contents
=================

   * [exchange 和 queue之间的绑定关系.](#exchange-和-queue之间的绑定关系)
   * [生产者只关心exchange, 消费者只关心queue](#生产者只关心exchange-消费者只关心queue)
   * [一个exchange可以binding多个queue, 通过routing key.](#一个exchange可以binding多个queue-通过routing-key)
   * [exchange](#exchange)
      * [Direct](#direct)
      * [Topic](#topic)
      * [fanout](#fanout)
   * [消息](#消息)
      * [可靠性](#可靠性)
         * [消息持久化到数据库中](#消息持久化到数据库中)
         * [延迟投递,二次确认,回调检查](#延迟投递二次确认回调检查)
      * [重复消费问题](#重复消费问题)
         * [唯一ID 指纹码,数据库主键去重](#唯一id指纹码数据库主键去重)
         * [Redis原子性](#redis原子性)
      * [confirm消息确认](#confirm消息确认)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*







# exchange 和 queue之间的绑定关系.
![image](https://user-images.githubusercontent.com/11831441/99941993-e931a580-2da9-11eb-9a43-1471dcd5ca04.png)

# 生产者只关心exchange, 消费者只关心queue
![image](https://user-images.githubusercontent.com/11831441/99943368-25fe9c00-2dac-11eb-832c-068199ec3b5f.png)

# 一个exchange可以binding多个queue, 通过routing key.
![image](https://user-images.githubusercontent.com/11831441/99943538-6b22ce00-2dac-11eb-8692-a2d62c37a719.png)

# exchange
![image](https://user-images.githubusercontent.com/11831441/100063153-b18b3200-2e6b-11eb-91a1-7900283e03a7.png)

## Direct
1. exchange不做任何处理,直接连接queue, routing_key需要和queue同名, 否则, message将丢弃.
2. rabbitmq 提供了一个默认的direct exchange, 如果exchange name 是空字符串, 那么将使用默认exchange.

## Topic 
\# 匹配一个或多个字符,包括"."
\* 只匹配一个字符, 包括"."
一条消息符合多个routing_key,将被分发给多个queue
但是一个queue, 只能接受一次消息

![image](https://user-images.githubusercontent.com/11831441/100068009-ec906400-2e71-11eb-877b-b9d92b0d4e76.png)

## fanout 
 不考虑routing_key. 将queue和exchange直连
![image](https://user-images.githubusercontent.com/11831441/100071193-be148800-2e75-11eb-99f1-a303788a466a.png)

# 消息
## 可靠性
### 消息持久化到数据库中
![image](https://user-images.githubusercontent.com/11831441/100073268-44ca6480-2e78-11eb-9240-5b6417e716e1.png)
### 延迟投递,二次确认,回调检查
减少二次落库次数
![image](https://user-images.githubusercontent.com/11831441/100074726-0fbf1180-2e7a-11eb-8b28-98fb3b085cac.png)

## 重复消费问题
### 唯一ID+指纹码,数据库主键去重
数据库压力大
### Redis原子性
redis和主数据库的原子性如何实现

## confirm消息确认
![image](https://user-images.githubusercontent.com/11831441/100079365-87dc0600-2e7f-11eb-83f1-cde4197d5c99.png)


