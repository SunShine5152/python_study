#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('*********函数式编程***********')
print('*********高阶函数***********')
#把函数作为参数传入，这样的函数称为高阶函数，函数式编程就是指这种高度抽象的编程范式。
def add(x,y,f):
    return f(x) + f(y)
print(add(-5,-7,abs))

print('*********map函数***********')
def f(x):
    return x * x
r = map(f,[1,2,3,4,5])
print(list(r))
print(list(map(str,[1,2,3,4,5])))

print('*********reduce函数***********')
from functools import reduce
def add(x,y):
    return x + y
print(reduce(add, [1,3,4,5]))

def fn(x,y):
    return x * 10 + y
print(reduce(fn, [1,3,4,5]))

digits = {'0':1,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
def str2num(str):
   def char2num(c):
       return digits[c]
   def calc(x,y):
       return x*10+y
   return reduce(calc,map(char2num,str))
print(str2num('666777888'))


print('***习题1***')
def normalize(name):
    return name[0].upper() + name[1:].lower()
# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))

print(L1)
print(L2)
print('***习题2***')
#L2 = normalize(L1)
# -*- coding: utf-8 -*-
from functools import reduce
def prod(L):
    def fn(x,y):
       return x * y
    return reduce(fn,L)
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')
#map是传入两个参数,一个函数,一个list,最后把函数作用于每个list元素,最后返回一个惰性list
#可以通过list()函数让它把结果做为一个序列返回.
#reduce是传入两个参数,一个函数是必须有两个参数,另一个是list,然后把list里每两个元素传入处理
#然后用得到的结果继续和下一个元素处理,最后得到一个结果,需要return返回.
print('***习题3***')
#-*- coding: utf-8 -*-
from functools import reduce
digits = {'0': 1, '1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
def str2float(s):
    def char2num(c):
        return digits[c]
    def calc(x,y):
        return x*10+y
    t = s.split('.')
    return reduce(calc, map(char2num, t[0])) + reduce(calc, map(char2num, t[1]))/10**len(t[1])

print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
     print('测试失败!')



