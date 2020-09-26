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


class Greenlet(greenlet):
    pass


def test3():
    print(12)
    gr2.switch()
    print(34)


def test4():
    print(56)
    gr1.switch()
    print(78)


gr1 = Greenlet(test3)
gr2 = Greenlet(test4)
gr1.switch()


import greenlet


def test1(x, y):
    z = gr2.switch(x + y)  # jump into test2
    print("test1 ", z)


def test2(u):
    print("test2 ", u)
    gr1.switch(10)  # z = 10


gr1 = greenlet.greenlet(test1)
gr2 = greenlet.greenlet(test2)
print(gr1.switch("hello", " world"))  # jump into test1

## test2  hello world
## test1  10
## None


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


if __name__ == "__main__":
    show_leak()
