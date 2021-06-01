#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('---------for---------')
names = ['lll','yyy','jjj']
for name in names:
    print(name)
print('---------for---------')
sum = 0
for x in [1,2,3,4,5,6,7,8,9,0]:
    sum = sum + x
print(sum)
print('---------for---------')
print(list(range(5)))

sum = 0
for x in range(101):
    sum = sum + x
print(sum)
print('---------while---------')
sum = 0
n = 99
while n>0:
    sum = sum + n
    n = n-2
print(sum)
print('---------break---------')
n = 1
while n <= 100:
    if n > 10:
        break
    print(n)
    n = n+1
print('END')
print('---------continue---------')
n = 0
while n < 10:
    n = n + 1
    if n % 2 == 0:
        continue
    print(n)
