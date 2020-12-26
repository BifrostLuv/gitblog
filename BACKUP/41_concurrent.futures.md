# [concurrent.futures](https://github.com/chaleaoch/gitblog/issues/41)


Table of Contents
=================



\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
 一个模仿Java的接口. 接口由抽象类`Executor`定义.

- 线程实现 - - ThreadPoolExecutor

- 进程实现 -- ProcessPoolExecutor

简单来说, 起一个线程池, 对submit进去的任务挨个执行. 执行的结果从Future获取. Future 是submit的返回值.

还需要一个死循环等所有任务执行结束

- concurrent.futures.as_completed(future_to_url)

- 或者concurrent.futures.wait

```text
import concurrent.futures
import urllib.request

URLS = [
    "http://www.foxnews.com/",
    "http://www.cnn.com/",
    "http://europe.wsj.com/",
    "http://www.bbc.co.uk/",
    "http://some-made-up-domain.com/",
]


# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print("%r generated an exception: %s" % (url, exc))
        else:
            print("%r page is %d bytes" % (url, len(data)))

```