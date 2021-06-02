#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('-------function:一些内置函数-----------')
print(abs(-111))
print(max(0,1,-1,5))
print(str(1.23))
print(float('1.23'))
print(bool(1))
#函数名起别名
a = abs
print(a(-211))
#习题
n1 = 255
n2 = 1000
T = (n1,n2)
for x in T:
    print('十六进制字符串表示：%s' %str(hex(x)))
print('-------function:函数定义-----------')
from myabs import myabs
print(myabs(-99))
#定义空函数,可以用作占位符,后续再写函数
def nop():
    pass
#pass还可以用在其他语句
age = 3
if age > 18:
    pass
print('-------function:函数可以返回多个值:实际是返回一个tuple-----------')
import math
def move(x,y,step,angle=0):
    nx = x + step*math.cos(angle)
    ny = y + step*math.sin(angle)
    return nx,ny
x,y = move(100,100,60,math.pi / 6)
print(x,y)
print('-------function:习题-----------')
def quadratic(a,b,c):
    if not isinstance(a,(int,float)):
        raise TypeError('bad operand type ')
    if not isinstance(b,(int,float)):
        raise TypeError('bad operand type ')
    if not isinstance(c,(int,float)):
        raise TypeError('bad operand type ')
    val1 = (-b+math.sqrt(b**2-(4*a*c)))/(2*a)
    val2 = (-b-math.sqrt(b**2-(4*a*c)))/(2*a)
    return val1,val2

print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))
if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')
print('-------function:函数参数:位置参数，默认参数-----------')
#默认参数可以简化函数的调用。设置默认参数时，有几点要注意：
#一是必选参数在前，默认参数在后，否则Python的解释器会报错（思考一下为什么默认参数不能放在必选参数前面）；
#二是如何设置默认参数。
#当函数有多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数。
#使用默认参数有什么好处？最大的好处是能降低调用函数的难度。
def power(x,n=2):
    s = 1
    while n > 0:
        n = n -1
        s = s * x
    return s

print(power(2))
print(power(2,3))

#定义默认参数要牢记一点：默认参数必须指向不变对象！
def add_end(L = []):
    L.append('END')
    return L
add_end()
add_end()
add_end()
print(add_end([]))
print(add_end([]))
print(add_end([]))
print('-------function:函数参数:可变参数-----------')
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc([1,2,3]))
print(calc([1,2,3,4]))

#利用可变参数简化调用方式
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc(1,2,3))#简化调用方式
print(calc(1,2,3,4))

nums = [1,2,3]
calc(nums[0], nums[1], nums[2])
calc(*nums)
print('-------function:函数参数:关键字参数-----------')
def person(name, age, **kv):
    print('name:',name,'age:',age,'other:',kv)

person('michael',30)
person('Bob',35,city='Beijing')
person('Adam',45,gender='M',job='Engineer')

print('------------------')
extra = {'city' : 'Beijing', 'job' : 'Engineer'}
person('Jack',23,city=extra['city'], job=extra['job'])
person('Jack',23,**extra)
print('-------function:函数参数:命名关键字参数-----------')
#如果要限制关键字参数的名字，就可以用命名关键字参数
def person(name, age, *, city, job):
    print(name, age, city, job)
person('Jack',24,**{'city':'Beijing'},job='Engineer')
#命名参数也可有默认参数
def person(name, age, *, city = 'Shanghai', job):
    print(name, age, city, job)
person('Jack',24,job='Engineer')
print('-------function:函数参数:参数组合-----------')
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)
def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)
#在函数调用的时候，Python解释器自动按照参数位置和参数名把对应的参数传进去。
f1(1,2)
f1(1, 2, c=3)
f1(1, 2, 3, 'a', 'b')
f1(1, 2, 3, 'a', 'b', x=99)
f2(1, 2, d=99, ext=None)
print('-------function:函数参数:参数组合,通过一个tuple和dict，你也可以调用上述函数：-----------')
#通过一个tuple和dict，也可以调用上述函数：
args = {1,2,3,4}
kw = {'d':99,'x':'#'}
f1(*args, **kw)

args = (1,2,3)
kw = {'d':88,'x':'w'}
f2(*args, **kw)
print('-------function:习题-----------')
def mul(*num):
    if num:
        s = 1
        for x in num:
            s = s * x
        return s
    else:
        raise TypeError
# 测试
print('mul(5) =', mul(5))
print('mul(5, 6) =', mul(5, 6))
print('mul(5, 6, 7) =', mul(5, 6, 7))
print('mul(5, 6, 7, 9) =', mul(5, 6, 7, 9))
if mul(5) != 5:
    print('测试失败1!')
elif mul(5, 6) != 30:
    print('测试失败2!')
elif mul(5, 6, 7) != 210:
    print('测试失败3!')
elif mul(5, 6, 7, 9) != 1890:
    print('测试失败4!')
else:
    try:
        mul()
        print('测试失败5!')
    except TypeError:
        print('测试成功6!')