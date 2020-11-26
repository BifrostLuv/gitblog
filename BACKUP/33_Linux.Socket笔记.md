# [Linux Socket笔记](https://github.com/chaleaoch/gitblog/issues/33)


Table of Contents
=================

   * [Socket 流程](#socket-流程)
      * [三次握手](#三次握手)
      * [四次挥手](#四次挥手)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*










# Socket 流程
![image](https://user-images.githubusercontent.com/11831441/100169202-d62fea00-2efd-11eb-99fc-d79cc3c30bf3.png)

## 三次握手
为什么要三次握手
发送方和接收方 
- 发送方去一次,接收方回一次这是一次成功的交互. 
- 接收方也会发送消息,发送方也需要应答.
- 接收方回的那一次和接收方发送的那一次可以合并成一次,就变成了三次握手.

## 四次挥手
四次挥手最大的问题是,如何合并,因为,可能存在一方想结束断开连接,但是另一方并不想断开.
![image](https://user-images.githubusercontent.com/11831441/100218973-6434c080-2f50-11eb-8b37-38ebfeda9b2c.png)

![image](https://user-images.githubusercontent.com/11831441/100237317-c0580e80-2f69-11eb-8481-63a82dfe3fe0.png)

ad2222222234444444