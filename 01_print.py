#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print(1000_0+1)
print("i'm ok")
print("i'm \"OK\"!")
print('\\\t\\')
print(r'\\\t\\')
print('''line1
line2
line3''')
n = 123
f = 456.789
s1 = 'Hello, world'
s2 = 'Hello, \'Adam\''
s3 = r'Hello, "Bart"'
s4 = r'''Hello,
Lisa!'''
print('hello',n)
print(f)
print('\'Hello, world\'')
print(r"'Hello, \'Adam\''")
print("r\'Hello, \"Bart\"\'")
print("r\'\'\'Hello,")
print('中文')
print('hello,%s' % 'world')
print('hi, %s, you have $%d.' % ('michael',1000))
print('hi, %s, you have $%s.' % ('michael',1000))
print('growth rate: %d %%' % 7)

s1 = 72
s2 = 85
name = 'xiaoming'
r = (s2-s1)/s1*100

print(f'hi, {name} you score high {r:.2f}% than before year')
print('小明的成绩提升了:{0:.1f}%'.format(r))
print('小明成绩提升了：%.1f %%' % r)