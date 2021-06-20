import sys

from PyQt5 import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class EventFilter(QDialog):
    def __init__( self, parent=None ):
        super(EventFilter, self).__init__(parent)
        self.setWindowTitle('事件过滤器')

        #实例化并设置四个标签文本
        self.label1 = QLabel('请点击')
        self.label2 = QLabel('请点击')
        self.label3 = QLabel('请点击')
        self.labelState = QLabel('test')

        #加载三个图片
        self.image1 = QImage('images\cartoon1.ico')
        self.image2 = QImage('images\cartoon2.ico')
        self.image3 = QImage('images\cartoon3.ico')

        self.width = 600
        self.height = 300

        #设置初始大小
        self.resize(self.width, self.height)

        #使用事假过滤器
        self.label1.installEventFilter(self)
        self.label2.installEventFilter(self)
        self.label3.installEventFilter(self)

        #设置窗口布局方式并添加控件
        layoyt = QGridLayout(self)
        layoyt.addWidget(self.label1, 500, 0)
        layoyt.addWidget(self.label2, 500, 1)
        layoyt.addWidget(self.label3, 500, 2)
        layoyt.addWidget(self.labelState, 600, 1)

    def eventFilter( self, watched, event ):
        #对事件一的处理过滤机制
        if watched == self.label1:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.labelState.setText('按下鼠标左键')
                elif mouseEvent.buttons() == Qt.MidButton:
                    self.labelState.setText('按下鼠标中间键')
                elif mouseEvent.buttons() == Qt.RightButton:
                    self.labelState.setText('按下鼠标右键')

                #转换图片大小
                transform=QTransform()
                transform.scale(0.5,0.5)
                tmp=self.image1.transformed(transform)
                self.label1.setPixmap(QPixmap.fromImage(tmp))
            if event.type()==QEvent.MouseButtonRelease:
                self.labelState.setText('释放鼠标按键')
                self.label1.setPixmap(QPixmap.fromImage(self.image1))
        return QDialog.eventFilter(self,watched,event)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    dialog=EventFilter()
    app.installEventFilter(dialog)
    dialog.show()
    app.exec_()