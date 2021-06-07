#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#对象包含了数据和函数等这些属性
#再python中所有的数据类型都可以当做对象，类似于面向对象中的类(Class)
#面向对象的设计思想是从自然界中来的，因为在自然界中，类（Class）
#和实例（Instance）的概念是很自然的。Class是一种抽象概念，比如
#我们定义的Class——Student，是指学生这个概念，而实例（Instance）则是一个个具体的Student
#类可以起到模板的作用，所以在创建实例的时候把一些我们认为必须绑定的属性强制填写进去，通过
#定义__init__方法，在创建实例的时候，就把属性绑上去。
#__init__方法的第一个参数永远是self，表示创建的实例本身，因此，在__init__方法内部，
#就可以把各种属性绑定到self，因为self就指向创建的实例本身。

#定义一个Student对象，也就是类class,包含name和score属性和print_score这个类的方法
#__init__方法的主要作用就是初始化这些属性。
print('***********类和实例***********')
# class Student(object):
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#
#     def print_score(self):
#         print('%s: %s' % (self.name, self.score))
# #创建具体的实例
# bart = Student('Bart Simpson', 59)
# lisa = Student('Lisa Simpson', 87)
# #实例开始活动
# bart.print_score()
# lisa.print_score()

#访问限制
# print('***********访问限制***********')
# bart.score = 90
# bart.print_score()
class Student(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))


bart = Student('Bart Simpson', 60)
bart.__score = 99
bart.__name = 'ace'
bart.print_score()

print('**************习题***************')
class Student(object):
    def __init__(self, name, gender):
        self.name = name
        self.__gender = gender
    def get_gender(self):
        return self.__gender
    def set_gender(self,gender):
        if gender.lower() in ['m', 'f', 'male', 'female']:
            self.__gender = gender
        else:
           raise Valueerror('Wrong gender')
# 测试:
bart = Student('Bart', 'male')
if bart.get_gender() != 'male':
    print('测试失败!')
else:
    bart.set_gender('female')
    if bart.get_gender() != 'female':
        print('测试失败!')
    else:
        print('测试成功!')
