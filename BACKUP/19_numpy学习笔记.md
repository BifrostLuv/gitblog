# [numpy学习笔记](https://github.com/chaleaoch/gitblog/issues/19)


Table of Contents
=================

   * [[[0.06161382 0.4935321  0.35183851 0.94555662]](#006161382-04935321--035183851-094555662)
   * [[0.39896273 0.34877886 0.57151596 0.20940768]]](#039896273-034877886-057151596-020940768)
   * [按行求和](#按行求和)
   * [[1.85254104 1.52866523]](#185254104-152866523)
   * [按行求和](#按行求和-1)
   * [[0.46057655 0.84231095 0.92335447 1.1549643 ]](#046057655-084231095-092335447-11549643-)
   * [合并](#合并)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
import numpy as np

array = np.array([[1, 2, 3], [3, 4, 5]])
print(array)
print(array.ndim)
print(array.shape)
print(array.size)

a = np.array([2, 3, 4], dtype=np.int)
print(a.dtype)


a = np.array([2, 3, 4], dtype=np.float)
print(a.dtype)

a = np.array([2, 3, 4], dtype=np.float32)
print(a.dtype)

a = np.zeros((3, 4), dtype=np.int)
print(a)

a = np.ones((3, 4), dtype=np.int)
print(a)

a = np.empty((3, 4), dtype=np.int)
print(a)

a = np.arange(10, 20, 2)
print(a)

a = np.arange(12)
print(a)

print(a.reshape((3, 4)))

a = np.linspace(1, 10, 20)
print(a)

a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

print(a + b)
print(a - b)
print(a * b)
print(a ** b)
print(a * 4)
print(a > 4)
print(a == 4)
print(np.sum(a))
print(np.min(a))
print(np.max(a))

c = np.random.random((2, 4))
print(c)
# [[0.06161382 0.4935321  0.35183851 0.94555662]
#  [0.39896273 0.34877886 0.57151596 0.20940768]]

# 按行求和
print(np.sum(c, axis=1))
# [1.85254104 1.52866523]

# 按行求和
print(np.sum(c, axis=0))
# [0.46057655 0.84231095 0.92335447 1.1549643 ]

print(np.average(a))

print(np.median(c))

print(np.cumsum(a))

print(a.reshape(2, 2).T)  # 转置矩阵

a = np.arange(10)
print(a)

b = a.reshape(2, 5)
print(b)
print(b[1])
print(b[1][0])
print(b[1, 0])
print(b[1, 2:])
print(b[b > 5])

# 合并
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.vstack((a, b)))
print(np.hstack((a, b)))

c = np.arange(12).reshape((3, 4))
print(c)
print(np.split(c, 2, axis=1))  # 垂直分割分成2份
print(np.split(c, 3, axis=0))  # 垂直分割分成2份
print(np.vsplit(c, 3))
print(np.hsplit(c, 2))

b = a.copy()


a = np.array([[1, 2, 3], [4, 5, 6]])

print(np.append(a, [7, 8, 9]))  # 变成一维数组
print(np.append(a, [[7, 8, 9]], axis=0))  # 二维数组,行追加
print(np.append(a, [[7], [8]], axis=1))  # 二维数组, 列追加

a = np.array([[1, 2], [3, 4], [5, 6]])
print(np.insert(a, 3, [11, 12]))
print(np.insert(a, 1, [11, 12], axis=0))
print(np.insert(a, 1, 11, axis=0))
print(np.insert(a, 1, [11, 12, 13], axis=1))
print(np.insert(a, 1, 12, axis=1))

a = np.arange(12).reshape(3, 4)
print(a)
print(np.delete(a, 5))
print(np.delete(a, 1, axis=1))
print(np.delete(a, np.s_[3:6]))


print(np.unique(a))
print(np.unique(a, return_index=True))
print(np.unique(a, return_counts=True))


a = np.array([[3, 7, 5], [8, 4, 3], [2, 4, 9]])
print(np.amin(a, 1))
print(np.amax(a, 0))

np.save("outputfile", a)
np.load("outputfile")
