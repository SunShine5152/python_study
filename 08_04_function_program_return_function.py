#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('*********函数式编程***********')
print('*********返回函数***********')
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
f1 = lazy_sum(1,2,3,4,5)
print(lazy_sum(1,2,3,4,5)())
print(f1())

def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
        print(fs)
    return fs
#每次循环都创建了一个新的函数,然后,把创建的3个函数都返回了.
f1, f2, f3 = count()
print(f1())
print(f2())
print(f3())
#全部都是9！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。


print('***改进****')
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1,4):
        fs.append(f(i))
        print(fs)
    return fs
f1,f2,f3=count()
print(f1())
print(f2())
print(f3())

print('***习题****')
def createCounter():
    i = 0
    def counter():
        nonlocal i
        i = i + 1
        return i
    return counter

# 测试:
counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')

print('*********匿名函数***********')
L = list(filter(lambda x : x%2 == 1, range(1,20)))
print(L)