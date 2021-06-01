#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('---------if---------')
#age = int(input('age:'))
age = 3
if age>18:
    print('adult')
elif age>=6:
    print('teenager')
else:
    print('kid')
print('---------if---------')
if 1:
    print('True')
print('---------practise---------')
height = 1.65
weight = 71
bmi = weight/(height*height)
print('bmi,%.1f' % bmi)
print('bmi {0:.1f}'.format(bmi))
print(f'bmi {bmi:.1f}')
if bmi<18.5:
    print('too light')
elif 18.5 < bmi < 25:
    print('normal')
elif 25 < bmi <28:
    print('too weight')
elif 28 < bmi <32:
    print('fat')
elif bmi > 32:
    print('too fat')