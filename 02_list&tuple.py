#!/usr/bin/env python3
# -*- coding: utf-8 -*
print('---------list---------')
classmates = ['Michael', 'Bob', 'Tracy']
print(classmates[0])
print(classmates[-1])
print('------------------')
classmates.append('lyj')
classmates.insert(1,'ace')
for name in classmates:
    print(name)
print('------------------')
classmates.pop()
classmates.pop(1)
for name in classmates:
    print(name)
print('------------------')
classmates[1] = 'ace'
for name in classmates:
    print(name)
print('--------tuple-----')
L = (1,2)
M = (1,)
N = ()
for name in L:
    print(name)
print('--------practise-----')
L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]

# 打印Apple:
print(L[0][0])
# 打印Python:
print(L[1][1])
# 打印Lisa:
print(L[2][2])
print('--------list和tuple是Python内置的有序集合，一个可变，一个不可变。根据需要来选择使用它们。-----')
