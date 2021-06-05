#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('*********函数式编程***********')
print('*********decorator***********')
print(int('12345'))
print(int('12345',base=8))
print(int('12345',base=16))

def int2(str, base = 2):
    return int(x,base)
#可以用偏函数做
import functools
int2 = functools.partial(int, base=2)
print(int2('1000000'))
print(int2('1000000',base=10))
