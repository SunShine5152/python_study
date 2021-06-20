# import sys
# from PyQt5.QtWidgets import QMessageBox,QPushButton,QApplication,QWidget


# def cbox():
#     QMessageBox.information(widget,'信息提示框','Ok 弹出测试信息')

# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     widget=QWidget()
#     cbox()
#     widget.show()
#     sys.exit(app.exec_()) 

# -*- coding: utf-8 -*-

"""
    【简介】
    内置的信号/槽示例


"""

# from PyQt5.QtWidgets import *
# import sys

# class Winform(QWidget):
#     def __init__(self,parent=None):
#         super().__init__(parent)
#         self.setWindowTitle('内置的信号/槽示例')
#         self.resize(330,  50 ) 
#         btn = QPushButton('关闭', self)
#         btn.clicked.connect(self.close) 

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = Winform()
#     win.show()
#     sys.exit(app.exec_())


# import sys
# from PyQt5.QtWidgets import *
# from functools import partial

# class WinForm(QMainWindow):
#     def __init__(self,parent=None):
#         super(WinForm, self).__init__(parent)
#         #实例化两个按钮
#         button1=QPushButton('Button1')
#         button2=QPushButton('Button2')

#         #todo 第一种方法
#         #单击信号关联槽函数，利用Lanbda表达式传递一个参数
#         # button1.clicked.connect(lambda :self.onButtonClick(1))
#         # button2.clicked.connect(lambda :self.onButtonClick(2))
#         #
#         #todo 第二种方法
#         button1.clicked.connect(partial(self.onButtonClick, 1))
#         button2.clicked.connect(partial(self.onButtonClick, 2))

#         #实例化窗口
#         main=QWidget()

#         #设置窗口的布局，并向其中添加控件
#         layout=QVBoxLayout(main)
#         layout.addWidget(button1)
#         layout.addWidget(button2)

#         #设置为中央控件
#         self.setCentralWidget(main)
#     def onButtonClick( self,n ):

#         #弹窗信息提示框，输出被点击的信息
#         print("Button {0}".format(n))
#         QMessageBox.information(self,'信息提示框','Button {0}'.format(n))
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     form=WinForm()
#     form.show()
#     sys.exit(app.exec_())


# import sys
# from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QPushButton
# from PyQt5 import QtCore

# class CustWidget(QWidget):
#     def __init__(self,parent=None):
#         super(CustWidget, self).__init__(parent)

#         #创建按钮，添加到自身窗口中
#         self.okButton=QPushButton('ok',self)
#         #使用setObjectName设置对象名称
#         self.okButton.setObjectName('okButton')

#         #设置自身的布局为水平布局，并添加按钮控件到其中
#         layout=QHBoxLayout(self)
#         layout.addWidget(self.okButton)


#         #TODo 第一种方法
#         #self.okButton.clicked.connect(self.okButton_clicked)

#     #def okButton_clicked( self ):
#     #   print('单击了ok按钮')

#         #第二种方法
#         QtCore.QMetaObject.connectSlotsByName(self)
#     @QtCore.pyqtSlot()
#     def on_okButton_clicked( self ):
#         print('单击了ok按钮')
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     win=CustWidget()
#     win.show()
#     sys.exit(app.exec_from PyQt5.QtCore import QObject,pyqtSignal


# from PyQt5.QtCore import QObject,pyqtSignal
# class SignalClass(QObject):
#     #声明无参数的信号
#     signal1=pyqtSignal()
#     #声明带一个int类型参数的信号
#     signal2=pyqtSignal(int)

#     def __init__(self,parent=None):
#         super(SignalClass, self).__init__(parent)
#         #将signal1信号连接到两个槽函数
#         self.signal1.connect(self.sig1Call)
#         self.signal1.connect(self.sig2Call)

#         #将signal2信号连接到信号1
#         self.signal2.connect(self.signal1)

#         #发射信号
#         self.signal1.emit()
#         self.signal2.emit(1)

#         #断开信号与槽函数的关系
#         self.signal1.disconnect(self.sig1Call)
#         self.signal1.disconnect(self.sig2Call)
#         self.signal2.disconnect(self.signal1)
#         print('**************')
#         #绑定信号与槽函数
#         self.signal1.connect(self.sig1Call)
#         self.signal2.connect(self.sigCall)

#         #信号发射
#         self.signal1.emit()
#         self.signal2.emit(1)
#     #输出信号1发射
#     def sig1Call( self ):
#         print('signal-1 emit')
#     #输出信号2发射
#     def sig2Call( self ):
#         print('signal-2 emit')
#     def sigCall( self,test):
#         print('signal %d'% test)
# if __name__ == '__main__':
#     signal=SignalClass()


