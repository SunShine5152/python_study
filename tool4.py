# -*- coding:utf-8 -*-
#QUIWin4K
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QStyleFactory
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QFormLayout, QGridLayout
from PyQt5.QtWidgets import QRadioButton, QCheckBox, QPushButton, QLineEdit, QLabel, QTextEdit, QMenuBar, QProgressBar,QComboBox

from PyQt5.QtCore import QObject, Qt, QSize, QRect, QRegExp,pyqtSignal, QEvent
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator
from PyQt5.Qt import QAction

class FocusLineEdit(QLineEdit):
#	focusIn  = pyqtSignal(object)
	focusOut = pyqtSignal(object)
	def __init__(self, parent=None):
		QLineEdit.__init__(self, parent)

	def focusInEvent(self, e):
		QLineEdit.focusInEvent(self, e)

	def focusOutEvent(self, e):
		self.focusOut.emit("FocusLineEdit")
		QLineEdit.focusOutEvent(self, e)

gSccbLineEditNames = {
# key: var_name
	'wid':'wid',
	'fdfe':'fdfeAddr',
	'rid':'rid',
	'data':'rData',
	'addr':'rAddr',
}
gFileLineEditNames = {
# key: var_name
	'txtfile':'txtFileName',
	'ramfile':'ramFileName',
	'romfile':'romFileName',
	'otpfile':'otpFileName',
}
gEmblLineEditNames = {
# key: dict,key
	'start0':('emblStart','0'),
	'start1':('emblStart','1'),
	'len0':('emblLen','0'),
	'len1':('emblLen','1'),
}
gImgLineEditNames = {
# key: var_name
	'hsize':'imgHsize',
	'vsize':'imgVsize',
}
gEmblLabelNames = {
# key: show_name
	'vcno':'VC',
	'len0':'Length',
	'len1':'Length',
}
gEmblCheckNames = {
# key: dict, key
	'emsel0':('emblSel','0'),
	'emsel1':('emblSel','1'),
}
gAllLabelNames = {
# key: show_name
	'dev':'Dev',
	'rid':'ID',
	'wid':'ID',
	'addr':'Addr',
	'data':'Data',
	'fdfe':'FDFE',
	'hsize':'Hsize',
	'vsize':'Vsize',
}
gAllCheckNames = {
# key show_name, var_name
	'romfile':('','romfileSelected'),
	'ramfile':('','ramfileSelected'),
	'txtfile':('','txtfileSelected'),
	'otpfile':('','otpfileSelected'),
	'autoBoot':('AutoBoot','bootMode'),
	'endian':('BigEndian','endianMode'),
	'tagen':('TagEnable', 'tagen'),
	'imgcrc':('Imgcrc', 'imgcrcen'),
	'save':('Imgsave', 'imgSave'),
	'display':('Display', 'displayen')
}
gComboDictNames = {
# key: var_name
	'mem':'memIdx',
	'dev':'devIdx',
	'loglv':'logLvIdx',
	'addrwid':'addrWidthIdx',
	'datawid':'dataWidthIdx',
	'vcno':'vcno',
#	'dp':'dpIdx',
#	'module':'mdIdx',
	'fmt':'fmtIdx',
	'otpdev':'otpdevIdx',
	'efuse':'efuseIdx',
}
gButtonDictNames = {
# key : show_name
	'txtopen':'OpenTxt',
	'ramopen':'OpenRam',
	'romopen':'OpenRom',
	'reload':'Reload',
	'download':'Download',
	'clear':'Clear',
	'fdfemap':'SetFeMode',
	'multiread':'MultiRead',
	'sendfile':'SendFile',
	'show':'Show',
#	'eshow':'ErrShow',
	'otpopen':'OtpOpen',
	'otpstart':'Start',
}

gImgFmtDict = {
	0:'YUV422-8',
	1:'YUV422-10',
	2:'YUV422-12',
	3:'YUV420-8',
	4:'YUV420-10',
	5:'YUV420-12',
	6:'RGB888',
	7:'RGB565',
	8:'RAW8',
	9:'RAW10',
	10:'RAW12',
	11:'RAW14',
	12:'RAW16',
	13:'RAW20',
	14:'RAW24',
}




def multiAddWidget(argLay, wdgList):
	for wdg in wdgList: argLay.addWidget(wdg)
	return argLay

class UI_mainWidget(QWidget):
	def __init__(self):
		super(UI_mainWidget, self).__init__()
		self.editDict = {}
		self.labelDict = {}
		self.comboDict = {}
		self.checkDict = {}
		self.buttonDict = {}

		self.__setupItems()
		self.__itemsCfg()
		self.__setupFont("Tahoma")
		self.__ignoreTabEvent()
		self.__setLayout()

	def __fileLogLayout(self):
		'''
		file and log layout
		'''
		def __checkLineButtonLay(nameList):
			tmpHLayout = QHBoxLayout()
			tmpHLayout.addWidget(self.checkDict[nameList[0]])
			tmpHLayout.addWidget(self.editDict[nameList[1]])
			tmpHLayout.addWidget(self.buttonDict[nameList[2]], 0, Qt.AlignRight | Qt.AlignVCenter)
			return tmpHLayout
		mainLayout = QVBoxLayout()
		mainLayout.addLayout(__checkLineButtonLay(['txtfile','txtfile','txtopen']))
		mainLayout.addLayout(__checkLineButtonLay(['ramfile','ramfile','ramopen']))
		mainLayout.addLayout(__checkLineButtonLay(['romfile','romfile','romopen']))
#		mainLayout.addWidget(self.__errGBox())
		mainLayout.addWidget(self.logTextEdit)
		mainLayout.addWidget(self.progressBar)
		return mainLayout

	def __ctrlLayout(self):
		'''
		control panel layout
		'''
		def __tmpGboxLayout(wdgSize, wdgList):
			tmpGbox = QGroupBox()
			tmpGbox.setMaximumSize(wdgSize)
			tmpGbox.setLayout(multiAddWidget(QHBoxLayout(),wdgList))
			return tmpGbox
		devSelRow = QHBoxLayout()
		devSelRow.addWidget(__tmpGboxLayout(QSize(70, 40),(self.labelDict['wid'],self.editDict['wid'])))
		devSelRow.addWidget(__tmpGboxLayout(QSize(100, 40),(self.labelDict['dev'],self.comboDict['dev'])))
		burnVLayout = QVBoxLayout()
		burnVLayout.addLayout(devSelRow)
		burnVLayout.addWidget(__tmpGboxLayout(QSize(200, 40),(self.checkDict['endian'],self.comboDict['loglv'])))
		burnVLayout.addWidget(__tmpGboxLayout(QSize(200, 40),(self.checkDict['autoBoot'],self.comboDict['mem'])))
		# main button layout
		thirdRow = QVBoxLayout()
		for key in ['reload','download','clear']: thirdRow.addWidget(self.buttonDict[key], 0, Qt.AlignVCenter)
		burnHLayout = QHBoxLayout()
		burnHLayout.addLayout(burnVLayout)
		burnHLayout.addLayout(thirdRow)
		return burnHLayout

	def __sccbGbox(self):
		'''
		sccb tool layout
		'''
		sccbLayout = QHBoxLayout()
		sccbGbox = QGroupBox("SCCBTool")
		sccbGbox.setFont(QFont("Tahoma"))
		forthRow = QVBoxLayout()
		forthRow.addLayout(multiAddWidget(QHBoxLayout(),(self.labelDict['fdfe'],self.editDict['fdfe'],self.fdfe16bitLabel)))
		forthRow.addLayout(multiAddWidget(QHBoxLayout(),(self.labelDict['rid'],self.editDict['rid'],self.ridWidthCombo)))
		forthRow.addLayout(multiAddWidget(QHBoxLayout(),(self.labelDict['addr'],self.editDict['addr'],self.comboDict['addrwid'])))
		forthRow.addLayout(multiAddWidget(QHBoxLayout(),(self.labelDict['data'],self.editDict['data'],self.comboDict['datawid'])))
		sccbLayout.addLayout(forthRow)
		sccbLayout.addLayout(multiAddWidget(QVBoxLayout(),(self.buttonDict['fdfemap'],self.buttonDict['multiread'],self.buttonDict['sendfile'])))
		sccbGbox.setLayout(sccbLayout)
		return sccbGbox

	def __emblGBox(self):
		def __emblLineLay(key):
			hlayout = QHBoxLayout()
			hlayout.addWidget(self.checkDict['emsel'+key],0, Qt.AlignLeft | Qt.AlignVCenter)
			hlayout.addWidget(self.editDict['start'+key],0, Qt.AlignLeft | Qt.AlignVCenter)
			hlayout.addWidget(self.labelDict['len'+key],0, Qt.AlignLeft | Qt.AlignVCenter)
			hlayout.addWidget(self.editDict['len'+key],0, Qt.AlignLeft | Qt.AlignVCenter)
			return hlayout
		mainLay = QVBoxLayout()
		rightLay = QVBoxLayout()
#		vcGBox =  QGroupBox()
#		vcGBox.setLayout(multiAddWidget(QHBoxLayout(), (self.labelDict['vcno'],self.comboDict['vcno'])))
		firstRow = multiAddWidget(QHBoxLayout(),(self.comboDict['fmt'],self.labelDict['vcno'],self.comboDict['vcno'] ,self.buttonDict['show']))
		thirdRow = multiAddWidget(QHBoxLayout(), (self.labelDict['hsize'],self.editDict['hsize'],self.labelDict['vsize'], self.editDict['vsize']))
		secondRow = multiAddWidget(QHBoxLayout(), (self.checkDict['tagen'], self.checkDict['imgcrc'], self.checkDict['save'], self.checkDict['display']))
		mainLay.addLayout(thirdRow)
		mainLay.addLayout(secondRow)
		mainLay.addLayout(firstRow)
		for key in ['0','1']:
			rightLay.addLayout(__emblLineLay(key))
		mainLay.addLayout(rightLay)
		emblGBox = QGroupBox("Embline")
		emblGBox.setFont(QFont("Tahoma"))
		emblGBox.setLayout(mainLay)
		return emblGBox

	def __otpGBox(self):
		mainLay = QVBoxLayout()
		firstRow = multiAddWidget(QHBoxLayout(), (self.checkDict['otpfile'], self.editDict['otpfile'], self.buttonDict['otpopen']))
		secondRow = multiAddWidget(QHBoxLayout(), (self.comboDict['otpdev'], self.comboDict['efuse'], self.buttonDict['otpstart']))
		mainLay.addLayout(firstRow)
		mainLay.addLayout(secondRow)
		otpGBox = QGroupBox("OTP")
		otpGBox.setFont(QFont("Tahoma"))
		otpGBox.setLayout(mainLay)
		return otpGBox

#	def __errGBox(self):
#		mainLay = QHBoxLayout()
#		errGBox = QGroupBox('Error')
#		errGBox.setFont(QFont("Tahoma"))
#		mainLay.addWidget(self.comboDict['dp'])
#		mainLay.addWidget(self.comboDict['module'])
#		mainLay.addWidget(self.buttonDict['eshow'])
#		errGBox.setLayout(mainLay)
#		return errGBox

	def __setLayout(self):
		mainLayout = QHBoxLayout()
		leftLayout = self.__fileLogLayout()
		rightLayout = QVBoxLayout()

		rightLayout.addLayout(self.__ctrlLayout())
		rightLayout.addWidget(self.__sccbGbox())
		rightLayout.addWidget(self.__emblGBox())
		rightLayout.addWidget(self.__otpGBox())

		mainLayout.addLayout(rightLayout)
		mainLayout.addLayout(leftLayout)
		self.setLayout(mainLayout)

	def __setupItems(self):
		for key in gSccbLineEditNames: self.editDict[key] = QLineEdit()
		for key in gFileLineEditNames: self.editDict[key] = QLineEdit()
		for key in gImgLineEditNames: self.editDict[key] = QLineEdit()
		for key in gAllLabelNames: self.labelDict[key] = QLabel(gAllLabelNames[key])
		for key in gComboDictNames: self.comboDict[key] = QComboBox()
		for key in gAllCheckNames: self.checkDict[key] = QCheckBox(gAllCheckNames[key][0])
		for key in "01": self.checkDict['emsel'+key] = QCheckBox('Start')
		for key in gButtonDictNames: self.buttonDict[key] = QPushButton(gButtonDictNames[key])
		for key in gEmblLabelNames: self.labelDict[key] = QLabel(gEmblLabelNames[key])
		for key in gEmblLineEditNames: self.editDict[key] = QLineEdit()
		self.ridWidthCombo = QComboBox()
		self.fdfe16bitLabel = QComboBox()
		self.editDict['addr'] = FocusLineEdit()
		self.logTextEdit = QTextEdit()			# test edit to show log
		self.progressBar = QProgressBar()		# progress bar to show progress of download

	def __itemsCfg(self):
		self.logTextHsize = 406
		self.buttonVsize = 30
		self.idEditHsize = 40
		self.comboDict['mem'].addItems(["rom", "ram"])
		self.comboDict['dev'].addItems(["GAIA", "Venus"])
		self.comboDict['addrwid'].addItems(["16bit", "32bit"])
		self.comboDict['datawid'].addItems(["8bit", "16bit", "32bit"])
		self.comboDict['loglv'].addItems(["Fatal", "Error", "Warning", "Info", "Debug"])
		self.comboDict['vcno'].addItems(['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'])
#		self.comboDict['dp'].addItems(['dp0','dp1','dp2','dp3'])
#		self.comboDict['module'].addItems(['ALL','MRX','IDC','IDP','RETIME','MTX'])
		self.comboDict['fmt'].addItems(list(gImgFmtDict.values()))
		self.comboDict['otpdev'].addItems(['OAX4K','X8B'])
		self.comboDict['efuse'].addItems(['efuse0', 'efuse1'])
#		self.comboDict['fmt'].addItems(['YUV422-8','YUV422-10','YUV422-12','YUV420-8','YUV420-10','YUV420-12',\
#			'RGB888','RGB565','RAW8','RAW10','RAW12','RAW14','RAW16','RAW20','RAW24'])
		for item in gFileLineEditNames: self.editDict[item].setReadOnly(True)
		self.ridWidthCombo.addItems(["8bit", "16bit"])
		self.fdfe16bitLabel.addItems(["16bit"])
		self.logTextEdit.setReadOnly(True)
		self.progressBar.setRange(0, 100)
		self.progressBar.setAlignment(Qt.AlignCenter)
		self.progressBar.setFormat("%p%")
		self.fdfe16bitLabel.setEnabled(False)
		self.buttonDict['fdfemap'].setChecked(False)
		self.ridWidthCombo.setEnabled(False)
		idRegExp = QRegExp('[0-9a-fA-F][02468aceACE]')
		self.editDict['wid'].setValidator(QRegExpValidator(idRegExp))
		self.editDict['rid'].setValidator(QRegExpValidator(idRegExp))
		self.editDict['fdfe'].setValidator(QRegExpValidator(QRegExp('[0-9a-fA-F]{,4}')))
		for key in gEmblLineEditNames: self.editDict[key].setValidator(QRegExpValidator(QRegExp('[0-9a-fA-F]{,4}')))
		for key in gImgLineEditNames: self.editDict[key].setValidator(QRegExpValidator(QRegExp('[0-9a-fA-F]{,4}')))
		self.logTextEdit.setMinimumSize(QSize(self.logTextHsize, 200))
		self.buttonDict['reload'].setMinimumSize(QSize(20, 40))
		self.buttonDict['download'].setMinimumSize(QSize(20, 40))
		self.buttonDict['sendfile'].setMinimumSize(QSize(20, 35))
		self.buttonDict['multiread'].setMinimumSize(QSize(20, 35))
		self.buttonDict['show'].setMinimumSize(QSize(60, 30))
		self.buttonDict['fdfemap'].setMinimumSize(QSize(20, 30))
		self.buttonDict['clear'].setMinimumSize(QSize(20, 40))
		self.editDict['rid'].setMaximumSize(QSize(100, 40))
		self.editDict['fdfe'].setMaximumSize(QSize(100, 40))
		for key in ['rid','fdfe','addr','data']: self.editDict[key].setMinimumSize(QSize(40, 26))
		for key in gAllLabelNames:
			if key not in ('dev','wid'): self.labelDict[key].setMinimumSize(QSize(20, 26))
		for key in gEmblLineEditNames:
			self.editDict[key].setMaximumSize(QSize(90, 26))
		for key in gImgLineEditNames:
			self.editDict[key].setMinimumSize(QSize(20, 24))
			self.editDict[key].setMaximumSize(QSize(90, 24))
		self.labelDict['vcno'].setMinimumSize(QSize(18, 26))
		self.labelDict['vcno'].setMaximumSize(QSize(30, 26))
		self.ridWidthCombo.setMinimumSize(QSize(20, 26))
		self.comboDict['addrwid'].setMinimumSize(QSize(20, 26))
		self.comboDict['datawid'].setMinimumSize(QSize(20, 26))
		self.fdfe16bitLabel.setMinimumSize(QSize(20, 26))
		self.editDict['wid'].setMaximumSize(QSize(self.idEditHsize, 20))
		self.comboDict['dev'].setMaximumSize(QSize(self.idEditHsize+15, 20))
		self.editDict['addr'].setMaximumSize(QSize(100, 40))
		self.editDict['data'].setMaximumSize(QSize(100, 40))
		self.buttonDict['fdfemap'].setCheckable(True)
		self.buttonDict['fdfemap'].setAutoExclusive(True)

	def __ignoreTabEvent(self):
		for key in gAllCheckNames: self.checkDict[key].setFocusPolicy(Qt.NoFocus)
		for key in '01': self.checkDict['emsel'+key].setFocusPolicy(Qt.NoFocus)
		for key in gButtonDictNames: self.buttonDict[key].setFocusPolicy(Qt.NoFocus)
		for key in gComboDictNames: self.comboDict[key].setFocusPolicy(Qt.NoFocus)
		for key in gFileLineEditNames: self.editDict[key].setFocusPolicy(Qt.NoFocus)
		for key in ['wid','rid','fdfe']: self.editDict[key].setFocusPolicy(Qt.ClickFocus)
		for key in gEmblLineEditNames: self.editDict[key].setFocusPolicy(Qt.ClickFocus)
		for key in gImgLineEditNames: self.editDict[key].setFocusPolicy(Qt.ClickFocus)
		self.logTextEdit.setFocusPolicy(Qt.ClickFocus)

	def __setupFont(self, strFont):
		normalFont = QFont(strFont)
		for key in gComboDictNames: self.comboDict[key].setFont(normalFont)
		for key in ['endian','autoBoot']: self.checkDict[key].setFont(normalFont)
		for key in gButtonDictNames: self.buttonDict[key].setFont(normalFont)
		for key in gAllLabelNames: self.labelDict[key].setFont(normalFont)
		for key in gEmblLabelNames: self.labelDict[key].setFont(normalFont)
		for key in gFileLineEditNames: self.editDict[key].setFont(normalFont)
		for key in gImgLineEditNames: self.editDict[key].setFont(normalFont)
		for key in gSccbLineEditNames:
			if key != 'wid': self.editDict[key].setFont(QFont(strFont, 11))
		for key in gEmblLineEditNames: self.editDict[key].setFont(QFont(strFont, 11))
		self.fdfe16bitLabel.setFont(normalFont)
		self.logTextEdit.setFont(QFont("Consolas",11))
		self.editDict['wid'].setFont(normalFont)

	def lockAllWidget(self, status):
		itemEn = not status
		for key in gAllCheckNames: self.checkDict[key].setEnabled(itemEn)
		for key in '01': self.checkDict['emsel'+key].setEnabled(itemEn)
		for key in gButtonDictNames: self.buttonDict[key].setEnabled(itemEn)
		for key in gComboDictNames: self.comboDict[key].setEnabled(itemEn)
		for key in gFileLineEditNames:self.editDict[key].setEnabled(itemEn)
		for key in gSccbLineEditNames:self.editDict[key].setEnabled(itemEn)
		for key in gEmblLineEditNames:self.editDict[key].setEnabled(itemEn)
		for key in gImgLineEditNames:self.editDict[key].setEnabled(itemEn)

	def fdfeLockWidget(self, status):
		itemEn = not status
		for key in gAllCheckNames: self.checkDict[key].setEnabled(itemEn)
		for key in '01': self.checkDict['emsel'+key].setEnabled(itemEn)
		for key in gComboDictNames: self.comboDict[key].setEnabled(itemEn)
		for key in gFileLineEditNames:self.editDict[key].setEnabled(itemEn)
		for key in ['txtopen','ramopen','romopen','download','reload','sendfile']:
			self.buttonDict[key].setEnabled(itemEn)
		self.editDict['wid'].setEnabled(itemEn)


class UI_embline(QWidget):
	logSignal = pyqtSignal(str)
	def __init__(self):
		super(UI_embline, self).__init__()
		self.setWindowTitle("Embline")
		self.infoTextEdit = QTextEdit(self)
		self.infoTextEdit.setFont(QFont("Consolas", 11))
		self.infoTextEdit.setMinimumSize(QSize(800, 600))
#		self.infoTextEdit.setSizePolicy()
		self.infoTextEdit.setReadOnly(True)
		self.setWindowModality(Qt.ApplicationModal)
		self.logSignal.connect(self.infoTextEdit.setText)

	def show(self):
		super().show()
		for i in range(10):
			self.display("hh {:d}".format(i))

	def display(self, logStr):
		self.logSignal.emit(logStr)


class UI_mainWindows(QMainWindow):
	def __init__(self):
		super(UI_mainWindows, self).__init__()
		self.mainSize = (730, 630)
		self.setFixedSize(QSize(*self.mainSize))
		self.centerWin = UI_mainWidget()
		self.setCentralWidget(self.centerWin)
		self.embWin = UI_embline()
		self.showMenu()
		self.show()

	def showMenu(self):
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("File")
		self.exitAppMenu = QAction("Exit", self)
		fileMenu.addAction(self.exitAppMenu)

		editMenu = mainMenu.addMenu("Edit")
		self.editLogMenu = QAction("Clearup", self)
		self.imgShowMenu = QAction("showimg", self)
		editMenu.addAction(self.editLogMenu)
		editMenu.addAction(self.imgShowMenu)

		helpMenu = mainMenu.addMenu("Help")
		self.helpInfoMenu = QAction("Help", self)
		helpMenu.addAction(self.helpInfoMenu)


class UI_about(QWidget):
	def __init__(self):
		super(UI_about, self).__init__()
		aboutSize = (453, 320)
		self.setWindowTitle("About")
		self.setFixedSize(QSize(*aboutSize))
		self.infoTextEdit = QTextEdit(self)
		self.infoTextEdit.setGeometry(QRect(0, 0, *aboutSize))
		self.infoTextEdit.setFont(QFont("Consolas", 11))
		self.infoTextEdit.setReadOnly(True)
		self.setWindowModality(Qt.ApplicationModal)
		self.show()

	def display(self, logStr):
		self.infoTextEdit.append(logStr)


if __name__ == '__main__':
	app = QApplication(sys.argv)
#    app.setStyle(QStyleFactory.create("Fusion"))
#    app.setStyle(QStyleFactory.create("Windows"))
#    app.setStyle(QStyleFactory.create("windowsvista"))
	UI = UI_mainWindows()
#	UI.show()
	sys.exit(app.exec_())
