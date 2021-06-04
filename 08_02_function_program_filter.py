#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('***函数式编程,高阶函数***')
print('***filter函数***')
def is_odd(n):
    return n % 2 == 1
L = [1,2,3,4,5,6,7,8,9]
print(list(filter(is_odd, L)))


def not_empty(s):
    return s and s.strip()

print(list(filter(not_empty, ['A', '', 'B', None, 'C', '  '])))
#filter把list传入函数,根据返回的bool决定元素的去留.

print('***习题***')
def is_palindrome(n):
    return str(n) == str(n)[::-1]
# 测试:
output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))
if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
    print('测试成功!')
else:
    print('测试失败!')