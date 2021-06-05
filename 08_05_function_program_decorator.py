#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('*********函数式编程***********')
print('*********decorator***********')
def now():
    print('***test***')
f = now
f()
print(now.__name__)
print(f.__name__)

print('****打印log*****')
def log(func):
    def wrapper1(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper1
@log#相当于now1=log(now1),之后调用now1()相当于执行行函数,即wrapper()
def now1():
    print('***ttttmp****')
now1()

print('***改进:可以传入打印参数***')
def log(text):
    def decorator(func):
        def wrapper2(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper2
    return decorator

@log('excute')
def now2():
    print('****555555555')

now2()
print(now.__name__)
print(now1.__name__)
print(now2.__name__)

print('***改进增加@functool*****')
print('****打印log*****')
import functools
def log(func):
    @functools.wraps(func)
    def wrapper1(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper1
@log#相当于now1=log(now1),之后调用now1()相当于执行行函数,即wrapper()
def now1():
    print('***ttttmp****')
now1()

print('***改进增加@functool*****')
print('***改进:可以传入打印参数***')
import functools
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper2(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper2
    return decorator

@log('excute')
def now2():
    print('****555555555')

now2()
print(now.__name__)
print(now1.__name__)
print(now2.__name__)


print('***习题***')
import time, functools
def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kw):
        start = time.time()
        res = fn(*args, **kw)
        end = time.time()
        t = (end - start) * 1000
        print('%s executed in %s ms' % (fn.__name__, t))
        return res
    return wrapper
# 测试
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;

@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;

f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')
else:
    print('测试成功!')


print('***思考题***')
import functools
def log(para):
    if isinstance(para, str):
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kw):
                print('%s call ' % para, wrapper.__name__)
                return fn(*args, **kw)
            return wrapper
        return decorator
    else:
        @functools.wraps(para)
        def wrapper(*args, **kw):
            print('call ', wrapper.__name__)
            return para(*args, **kw)
        return wrapper

@log('just')
def abc():
    print('abc')
    return 0
@log
def cba():
    print('cba')
    return 0

abc()
cba()