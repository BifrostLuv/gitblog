# [Python 的线程同步](https://github.com/chaleaoch/gitblog/issues/46)


Table of Contents
=================

   * [R锁](#r锁)
   * [condition](#condition)
      * [原理](#原理)
      * [实例方法](#实例方法)
      * [例子](#例子)
   * [event](#event)
   * [信号量](#信号量)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
# R锁

Reentrant Lock 可重入锁

1. 谁拿到谁释放。如果线程A拿到锁，线程B无法释放这个锁，只有A可以释放；

2. 同一线程可以多次拿到该锁，即可以acquire多次；

3. acquire多少次就必须release多少次，只有最后一次release才能改变RLock的状态为unlocked）

```text
lock = threading.RLock()
lock.acquire
lock.release
```

# condition

主动休眠,被动唤醒

- 和锁相比, 多了一个wait和notify. 

- 锁是无序的,线程1将锁释放,还可能再次获得锁. 

- 但是条件变量,可以通知其他线程,被动的将其他线程唤醒,

- 同时自己主动休眠,等待其他线程唤醒.

## 原理

- wait的时候,会将自己锁住,然后将锁放入一个队列中. 并释放公共锁.

- notify的时候,会从列表中取出若干个锁,release.

- 为了防止死锁, 使用wait 之前需要先调用acquire -- 也就是wait中提到的公共锁.

    - 两个线程都将自己锁住(wait), 并等待对方notify(release)就死锁了. -- 死锁的条件

## 实例方法

```text
acquire([timeout])/release(): 调用关联的锁的相应方法。 
wait([timeout]): 调用这个方法将使线程进入Condition的等待池等待通知，并释放关联的锁。
使用前线程必须已获得锁定，否则将抛出异常。 
notify(n=1): 调用这个方法将从等待池挑选n个线程并通知，收到通知的线程将自动调用
acquire()尝试获得锁定（进入锁定池）；其他线程仍然在等待池中。调用这个方法不会
释放锁定。使用前线程必须已获得锁定，否则将抛出异常。 
notifyAll(): n=len(所有的锁队列)
```

## 例子

```python
import threading
class XiaoAi(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="小爱")
        self.cond = cond

    def run(self):
        self.cond.acquire()

        self.cond.wait()
        print("{} : 在".format(self.name))
        self.cond.notify()

        self.cond.wait()
        print("{} : 好啊".format(self.name))
        self.cond.notify()

        self.cond.wait()
        print("{} : 不聊了，再见".format(self.name))
        self.cond.notify()

        self.cond.release()


class TianMao(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="天猫精灵")
        self.cond = cond

    def run(self):
        self.cond.acquire()

        print("{} : 小爱同学".format(self.name))
        self.cond.notify()
        self.cond.wait()

        print("{} : 我们来对古诗吧".format(self.name))
        self.cond.notify()
        self.cond.wait()

        print("{} : 我住长江头".format(self.name))
        self.cond.notify()
        self.cond.wait()

        self.cond.release()

if __name__ == "__main__":
    cond = threading.Condition()
    xiaoai = XiaoAi(cond)
    tianmao = TianMao(cond)
    
    xiaoai.start()
	tianmao.start()
```

# event

一个线程发出事件信号，而其他线程等待该信号。

- set 可将其设置为true。

- clear 设置false

- wait 方法将进入阻塞直到标识为true。

- 标识初始时为 false 。

# 信号量

用于限制并发数量

一个信号量管理一个内部计数器，该计数器因 `acquire()` 方法的调用而递减，因 `release()` 方法的调用而递增。 计数器的值永远不会小于零；当 `acquire()` 方法发现计数器为零时，将会阻塞，直到其它线程调用 `release()` 方法。





