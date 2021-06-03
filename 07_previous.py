#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('---------构造一个列表---------')
L = []
n = 1
while n <= 20:
    L.append(n)
    n = n+1
print(L)

print('--------slice----------')
print(L[1:5])
print(L[:5])
print(L[-2:])
print(L[-2:-1])
print(L[:10:2])
print(L[::5])
print(L[:])
M = []
M = L[:]
print(M)
T = (1,2,3,4,5,6)
print(T[1:3])
str = 'abcdefg'
print(str[1:3])

print('--------slice:习题----------')
def trim(s):
    i=0
    j=-1
    l=len(s)
    while l > 0:
        if s[i] == ' ':
            i = i+1
            l = l-1;
        else:
            break
    while l > 0:
        if s[-1] != ' ':
            return s[i:]
        if s[j] == ' ':
            j = j - 1
            l = l - 1;
        else:
            break
    return s[i:j+1]

print(len('  asdf   '))
print(len(trim('  asdf   ')))
print(trim('  asdf   '))
# 测试:
if trim('hello  ') != 'hello':
    print('测试失败1!')
elif trim('  hello') != 'hello':
    print('测试失败2!')
elif trim('  hello  ') != 'hello':
    print('测试失败3!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败4!')
elif trim('') != '':
    print('测试失败5!')
elif trim('    ') != '':
    print('测试失败6!')
else:
    print('测试成功7')

print('--------Iteration----------')
d = {'a':1,'b':2,'c':3}
for key in d:
    print(key)
for key in d.values():
    print(key)
for k,v in d.items():
    print(k,v)
#判断是否可以迭代
from collections.abc import Iterable
print(isinstance('abc', Iterable))
print(isinstance([1,2,3], Iterable))
print(isinstance(123, Iterable))
#Python内置的enumerate函数可以把一个list变成索引-元素对，这样就可以在for循环中同时迭代索引和元素本身
for i,value in enumerate(['A', 'B', 'C']):
    print(i,value)
L = ['a', 'b', 'c']
for i,value in enumerate(L):
    print(i,value)
print('--------Iteration:习题----------')
def findMinAndMax(L):
    if len(L) == 0:
        return None, None
    elif len(L) == 1:
        return L[0], L[0]
    else:
        min = L[0]
        max = L[0]
        for v in L:
            if v > max:
                max = v
            elif v < min:
                min = v
        return min, max

# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')

print('************ List Comprehensions:列表生成式***************')
print(list(range(2,11)))

L = []
for x in range(1,11):
    L.append(x * x)
print(L)
#也可以用下面一句话替换
print([x*x for x in range(1,11)])
#也可以加上判断，筛选出偶数的平方
print([x*x for x in range(1,11) if x % 2 == 0])
#还可以使用两层循环，可以生成全排列
print([m+n for m in 'ABC' for n in 'XYZ'])

#列出当前所有的文件夹
import os
print([d for d in os.listdir('.')])
#列表生成式也可以使用两个变量来生成list
d = {'x':'A','y':'B','z':'C'}
print([k + '=' + v for k, v in d.items()])
#把一个list中的所有字符串变成小写
L = ['Hello', 'World', 'IBM', 'Apple']
print([s.lower() for s in L])
print([x if x % 2 == 0 else -x for x in range(1,11)])

# print('***********习题**************')
# L1 = ['Hello', 'World', 18, 'Apple', None]
# L2 = [x.lower() for x in L1 if isinstance(x,str)]
# print(L2)
# if L2 == ['hello', 'world', 'apple']:
#     print('测试通过!')#不知为何这段必须放在其他文件可以通过，本文件报错。
# else:
#     print('测试失败!')

print('***********列表生成器**************')
L = [x for x in range(10)]
print(L)
g = (x for x in range(10))
print(next(g))
print(next(g))
print(next(g))
print('***********for**************')
for x in g:
    print(x)
print('***fib***')
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n = n + 1
    return 'done'
print(fib(6))
#yield 调试
def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)
g = foo()
print(next(g))
print("*"*20)
print(next(g))
print(next(g))
print(next(g))

#send方法debug
def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)
g = foo()
print(next(g))
print("*"*20)
print(g.send(7))
print(next(g))
print(next(g))
print(g.send(6))

for n in range(11):
    a=n
    print(a)

def foo(num):
    print("starting111...")
    while num<10:
        num=num+1
        yield num
for n in foo(0):
    print(n)

#斐波拉契数列生成器
print('***fib gnerator***')
def fib(max):
    n,a,b = 0,0,1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'
g = fib(6)
#用生成器打印fib列表并拿到fib(max)的return值done
def print_g():
    while True:
        try:
            x = next(g)
            print('g:', x)
        except StopIteration as e:
            print('Generator return value:', e.value)
            break
print_g()
print('***yanghui sanjiao ****')
def triangles():
    L =[1]
    while True:
        yield L[:]
        L.append(0)
        L=[L[i]+L[i-1] for i in range(len(L))]
n = 0
results = []
for t in triangles():
    results.append(t)
    n = n + 1
    if n == 10:
        break

for t in results:
    print(t)

if results == [
    [1],
    [1, 1],
    [1, 2, 1],
    [1, 3, 3, 1],
    [1, 4, 6, 4, 1],
    [1, 5, 10, 10, 5, 1],
    [1, 6, 15, 20, 15, 6, 1],
    [1, 7, 21, 35, 35, 21, 7, 1],
    [1, 8, 28, 56, 70, 56, 28, 8, 1],
    [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
]:
    print('测试通过!')
else:
    print('测试失败!')