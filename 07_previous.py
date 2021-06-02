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