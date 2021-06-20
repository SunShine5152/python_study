import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class WinForm(QWidget):
    def __init__(self):
        super(WinForm, self).__init__()
        self.initUI()
    def initUI( self ):
        #先创建水平滑块和Lcd控件
        lcd=QLCDNumber(self)
        slider=QSlider(Qt.Horizontal,self)

        #垂直布局，添加控件
        vbox=QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(slider)

        #设置窗口布局
        self.setLayout(vbox)
        #设置滑块数值信号改变连接Lcd的更新
        slider.valueChanged.connect(lcd.display)

        #设置初始位置以及初始大小，设置标题
        self.setGeometry(300,300,350,150)
        self.setWindowTitle('信号与槽：连接滑块LCd')
if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=WinForm()
    form.show()
    sys.exit(app.exec_())