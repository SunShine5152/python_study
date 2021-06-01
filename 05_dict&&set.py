#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('---------dict---------')
dct = {'ll':00,'yy':11,'jj':22}
print(dct)
for name in dct:
    print(dct[name])

print('---------dict:单独初始化值---------')
dct['jj'] = 33
print(dct)
print('---------dict:判断key是否存在---------')
print('aaa' in dct)
print('ll' in dct)
print(dct.get('yy'))
print(dct.get('aaa',-1))
print('---------dict:删除key---------')
dct.pop('yy')
print(dct)
print('********Python 中的集合，和数学中的集合概念一样，用来保存不重复的元素，即集合中的元素都是唯一的，互不相同。****')
print('---------set---------')
s = set([1,2,3])#第一种创建方法
s1 = {1,2,3,6}#第二种创建方法
print(s)
print(s1)
s = set([1,2,2,3,3])
print(s)
s.add(4)
s.add(3)
print(s)
s.remove(4)
print(s)
print('---------set:交集，并集---------')
s1 = set([1,2,3])
s2 = set([1,2,4])
print(s1&s2)
print(s1|s2)
print('---------可变和不可变对象---------')
a = ['c','b','a']
a.sort()
print(a)

a = 'abc'
b = a.replace('a','A')
print(a)
print(b)
print('-------set-----------')
s1 = set([1,2,3])
s2 = set((1,2,3))
print(s1)
print(s2)
s3 = set([1,(2,3)])
s4 = {1,'c',1,(1,2,3),'c'}
print(s4)
print('***set() 函数为 Python 的内置函数，其功能是将字符串、列表、元组、range 对象等可迭代对象转换成集合。***')
s5 =set((1,'c',1,(1,2,3),'c'))
print(s5)
