import gevent


def foo():
    print("Running in foo")
    gevent.sleep(0)
    print("Explicit context switch to foo again")


def bar():
    print("Explicit context to bar")
    gevent.sleep(0)
    print("Implicit context switch back to bar")


gevent.joinall(
    [
        gevent.spawn(foo),
        gevent.spawn(bar),
    ]
)


# Running in foo
# Explicit context to bar
# Explicit context switch to foo again
# Implicit context switch back to bar


import time
import gevent
from gevent import select

start = time.time()
tic = lambda: "at %1.1f seconds" % (time.time() - start)


def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print("Started Polling: %s" % tic())
    select.select([], [], [], 2)
    print("Ended Polling: %s" % tic())


def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print("Started Polling: %s" % tic())
    select.select([], [], [], 2)
    print("Ended Polling: %s" % tic())


def gr3():
    print("Hey lets do some stuff while the greenlets poll, %s" % tic())
    gevent.sleep(1)


gevent.joinall(
    [
        gevent.spawn(gr1),
        gevent.spawn(gr2),
        gevent.spawn(gr3),
    ]
)
