# [greenlet(1) 使用](https://github.com/chaleaoch/gitblog/issues/4)


Table of Contents
=================

   * [Greenlet(1) 使用](#greenlet1-使用)
      * [初体验](#初体验)
      * [带参数的greenlet](#带参数的greenlet)
      * [greenlet的parent](#greenlet的parent)
      * [Greenlet生命周期](#greenlet生命周期)
      * [如何结束生命周期](#如何结束生命周期)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
# Greenlet(1) 使用


## 初体验

```go
#! /usr/bin/python3
# -*- encoding: utf-8 -*-

from greenlet import greenlet


def test1():
    print(12)
    gr2.switch()
    print(34)


def test2():
    print(56)
    gr1.switch()
    print(78)


gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()

# 12
# 56
# 34
```

- greenlet就是协程切换, 和python原生协程和生成器相比, greenlet的协程可以随意切, 原生只能往回(父亲)切.

  - 必须单线程多协程任意切换, 如果切到别的线程会报错.

- greenlet是一个纯C项目,通过[python C api](https://docs.python.org/zh-cn/3/c-api/index.html)实现的python模块.

- 原理是通过汇编切换当前栈帧实现.

  - 先切换

    ![1601127567683](Greenlet(1) 使用.assets/1601127567683.png)

  - 后管理

![1601127492315](Greenlet(1) 使用.assets/1601127492315.png)

​	具体也不是很懂.后面弄清楚了在更新.

- 上面代码 `print(78)` 没有打印出来会导致内存泄漏, 后面会介绍解决办法.
- greenlet是一个类

## 带参数的greenlet

```go
import greenlet


def test1(x, y):
    z = gr2.switch(x + y) # jump into test2 
    print("test1 ", z)


def test2(u):
    print("test2 ", u)
    gr1.switch(10) # z = 10


gr1 = greenlet.greenlet(test1)
gr2 = greenlet.greenlet(test2)
print(gr1.switch("hello", " world")) # jump into test1

## test2  hello world
## test1  10
## None
```

## greenlet的parent

- greenlet的parent是由创建的地方决定的,而不是调用的地方.

- 协程正常执行结束,会跳转回parent.

  ```go
  import greenlet
  
  
  def test1(x, y):
      print(id(greenlet.getcurrent()), id(greenlet.getcurrent().parent))  # 40240272 40239952
      z = gr2.switch(x + y)
      print("back z", z)  # 这里没有输出
  
  
  def test2(u):
      print(id(greenlet.getcurrent()), id(greenlet.getcurrent().parent))  # 40240352 40239952
      return "hehe"  # 跳转回main
  
  
  gr1 = greenlet.greenlet(test1)  # parent is main
  gr2 = greenlet.greenlet(test2)  # parent is main
  print(id(greenlet.getcurrent()), id(gr1), id(gr2))  # 40239952, 40240272, 40240352
  print(gr1.switch("hello", " world"), "back to main")  # hehe back to main
  ```

- 协程中抛出异常,也会传递给parent.

  ```Go
  import greenlet
  
  def test1(x, y):
      try:
          z = gr2.switch(x + y)
      except Exception:
          print("catch Exception in test1")
  
  
  def test2(u):
      assert False  # 异常传到给main
  
  
  gr1 = greenlet.greenlet(test1)
  gr2 = greenlet.greenlet(test2)
  try:
      gr1.switch("hello", " world")
  except:
      print("catch Exception in main")
  ```

## Greenlet生命周期

```
from greenlet import greenlet


def test1():

    gr2.switch(1)
    print("test1 finished")


def test3():
    print(123)


def test2(x):
    y = gr3.switch()
    print("test2 first", x)
    print("test2 first y", y)
    z = gr1.switch()
    print("test2 back", z)


gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr3 = greenlet(test3)
gr3.switch()
gr1.switch()
print("gr1 is dead?: %s, gr2 is dead?: %s" % (gr1.dead, gr2.dead))
gr2.switch(3)
print("gr1 is dead?: %s, gr2 is dead?: %s" % (gr1.dead, gr2.dead))
print(gr2.switch(10))  # parent greenlet
```

- 执行完毕的协程 完成声明周期 dead
- 如果已经dead, 继续调用switch, 将调用parent greenlet

## 如何结束生命周期

```
from greenlet import greenlet, GreenletExit

huge = []


def show_leak():
    def test1():
        gr2.switch()

    def test2():
        huge.extend([x * x for x in range(100)])
        try:
            gr1.switch()
        finally:
            print("finish switch del huge")
            del huge[:]

    gr1 = greenlet(test1)
    gr2 = greenlet(test2)
    gr1.switch()
    gr1 = gr2 = None  # 这里触发GreenletExit, GreenletExit这个异常并不会抛出到parent，所以main greenlet也不会出异常
    print("length of huge is zero ? %s" % len(huge))
```

参考: 

https://www.cnblogs.com/xybaby/p/6337944.html

https://greenlet.readthedocs.io/en/latest/

本文代码可以在[这里](https://github.com/chaleaoch/gitblog/blob/master/src/greenlet1.py)找到