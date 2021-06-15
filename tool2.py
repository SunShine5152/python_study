# -*- coding:utf-8 -*-
#QSlot4K
import sys, os
import time as tm
import functools as ftool
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtCore import pyqtSignal,QSize,QRegExp,Qt,QTimer
from PyQt5.QtGui import QRegExpValidator,QColor
from PyQt5.Qt import QObject

try:
	from QUI.QUIWin4K import *
	from QUI.QUI_thread import WorkThread
	import Util
except ModuleNotFoundError:
	from QUIWin4K import *
	from QUI_thread import WorkThread

gLogDist = {
	0:'',
	1:"Fatal-> ",
	2:"Error-> ",
	3:"Warning-> ",
	4:"Info-> ",
	5:"Debug-> ",
}

gSignalDict = {}


def combBytes(datList):
	length, retDat = len(datList), 0
	for i in range(length): retDat |= datList[i] << (8*(length-i-1))
	return retDat


def getDictKey(item, itemDict):
	for key, tmpitem in itemDict.items():
		if tmpitem==item:
			return key
	return False

class QSlotMain(UI_mainWindows):

	logSignal = pyqtSignal(tuple)                      # signal for log print
	imgShowSignal = pyqtSignal(tuple)					# signal for log print
	# use signal to write LineEdit
	progressSignal = pyqtSignal(object)                 # signal for log progress bar
	txtfileEditSignal = pyqtSignal(object)              # signal for file edit
	ramfileEditSignal = pyqtSignal(object)              # signal for file edit
	romfileEditSignal = pyqtSignal(object)              # signal for file edit
	otpfileEditSignal = pyqtSignal(object)				# signal for file edit

	# line edit up or down signal
	widUDSignal = pyqtSignal(object)
	ridUDSignal = pyqtSignal(object)
	addrUDSignal = pyqtSignal(object)
	dataUDSignal = pyqtSignal(object)
	fdfeAddrUDSignal = pyqtSignal(object)

	#embl edit up or down signal
	#(key, str)
	emblStartUDSignal = pyqtSignal(str)
	emblLenUDSignal   = pyqtSignal(str)

	ramOpenSignal = pyqtSignal(str)
	romOpenSignal = pyqtSignal(str)
	txtOpenSignal = pyqtSignal(str)
	otpOpenSignal = pyqtSignal(str)
	sendFileSignal = pyqtSignal(str)
	ramOpenButtonSignal = pyqtSignal(str)
	romOpenButtonSignal = pyqtSignal(str)
	txtOpenButtonSignal = pyqtSignal(str)
	otpOpenButtonSignal = pyqtSignal(str)
	sendFileButtonSignal = pyqtSignal(str)

	# widget lock signal
	itemsLockSignal = pyqtSignal(bool)
	fdfeLockSignal = pyqtSignal(bool)

	LOG_NONE	= 0
	LOG_FATAL	= 1
	LOG_ERROR	= 2
	LOG_WARNING = 3
	LOG_INFO	= 4
	LOG_DEBUG	= 5

	def __init__(self):
		super(QSlotMain, self).__init__()
		for key in gSccbLineEditNames: setattr(self, gSccbLineEditNames[key], -1)
		for key in gComboDictNames: setattr(self, gComboDictNames[key], 0)
		self.endianMode = 1
		self.tagen = 0
		self.imgSave = 0
		self.displayen = 0
		self.emblLen = {}
		self.emblStart = {}
		self.emblSel = {}
		for key in '01234':
			self.emblLen[key] = -1
			self.emblSel[key] = 0
			self.emblStart[key] = -1

        # use for slot function
		self.slotThread = WorkThread()
		self._addSignalDict()
		self.__connectSlot()
		self.addrCombSlot()
		self.dataCombSlot()

	def __connectSlot(self):
		# register slot function
		# push button
		self.centerWin.buttonDict['ramopen'].clicked.connect(lambda:self.signalEmit('ramopen', os.path.dirname(self.ramFileName)))
		self.centerWin.buttonDict['romopen'].clicked.connect(lambda:self.signalEmit('romopen', os.path.dirname(self.romFileName)))
		self.centerWin.buttonDict['txtopen'].clicked.connect(lambda:self.signalEmit('txtopen', os.path.dirname(self.txtFileName)))
		self.centerWin.buttonDict['otpopen'].clicked.connect(lambda:self.signalEmit('otpopen', os.path.dirname(self.otpFileName)))
		self.centerWin.buttonDict['sendfile'].clicked.connect(lambda:self.signalEmit('sendfile', os.path.dirname(self.snrFileName)))

		self.centerWin.buttonDict['multiread'].clicked.connect(lambda:self.addThread(self.mulitReadBTSlot))
		self.centerWin.buttonDict['reload'].clicked.connect(lambda:self.addThread(self.reloadButtonSlot))
		self.centerWin.buttonDict['download'].clicked.connect(lambda:self.addThread(self.downloadButtonSlot))
		self.centerWin.buttonDict['otpstart'].clicked.connect(lambda:self.addThread(self.otpstartButtonSlot))
		self.centerWin.buttonDict['clear'].clicked.connect(self.centerWin.logTextEdit.clear)
		self.centerWin.buttonDict['fdfemap'].clicked.connect(self.fdfeMapSlot)
		self.centerWin.buttonDict['show'].clicked.connect(lambda:self.addThread(self.emblShowSlot))
#		self.centerWin.buttonDict['show'].clicked.connect(self.embWin.show)
#		self.centerWin.buttonDict['eshow'].clicked.connect(self.errShowSlot)
		# check button
		for key in gAllCheckNames: self.centerWin.checkDict[key].toggled.connect(ftool.partial(self.getCheckValue,key))
		# comb box
		self.centerWin.comboDict['vcno'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['vcno'], 'vcno'))
		self.centerWin.comboDict['loglv'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['loglv'], 'logLvIdx'))
		self.centerWin.comboDict['mem'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['mem'], 'memIdx'))
#		self.centerWin.comboDict['dp'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['dp'], 'dpIdx'))
#		self.centerWin.comboDict['module'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['module'], 'mdIdx'))
		self.centerWin.comboDict['fmt'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['fmt'], 'fmtIdx'))
		self.centerWin.comboDict['otpdev'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['otpdev'], 'otpdevIdx'))
		self.centerWin.comboDict['efuse'].currentTextChanged.connect(lambda:self.getCombValue(self.centerWin.comboDict['efuse'], 'efuseIdx'))
		self.centerWin.comboDict['dev'].currentTextChanged.connect(self.devComboSlot)
		self.centerWin.comboDict['addrwid'].currentTextChanged.connect(self.addrCombSlot)
		self.centerWin.comboDict['datawid'].currentTextChanged.connect(self.dataCombSlot)

		for key in gEmblCheckNames:
			self.centerWin.checkDict[key].toggled.connect(lambda x,y=key:self.getEmblCheck(self.emblSel, y))

		# line edit slot
		for key in gFileLineEditNames: self.centerWin.editDict[key].textChanged.connect(self.fileNameSlot)
		for key in gSccbLineEditNames:
			self.centerWin.editDict[key].textChanged.connect(lambda x, y=key: self.txtChangedSlot(gSccbLineEditNames[y], x))
			self.centerWin.editDict[key].textEdited.connect(ftool.partial(self.editUpperSlot, key))
		for key in gEmblLineEditNames:
			self.centerWin.editDict[key].textChanged.connect(lambda x, y=key: self.txtChangedSlot(gEmblLineEditNames[y], x))
			self.centerWin.editDict[key].textEdited.connect(ftool.partial(self.editUpperSlot, key))
		for key in gImgLineEditNames:
			self.centerWin.editDict[key].textChanged.connect(lambda x, y=key: self.txtChangedSlot(gImgLineEditNames[y], x))
			self.centerWin.editDict[key].textEdited.connect(ftool.partial(self.editUpperSlot, key))
		# enter data to value
		self.centerWin.editDict['data'].returnPressed.connect(lambda:self.addThread(self.dataLineEnter))
		self.centerWin.editDict['fdfe'].returnPressed.connect(lambda:self.addThread(self.fdfeLineEnter))

		# menu
		self.helpInfoMenu.triggered.connect(self.setupAboutUI)
		self.exitAppMenu.triggered.connect(self.close)
		self.editLogMenu.triggered.connect(self.imgClearup)
		self.imgShowMenu.triggered.connect(self.showImgSlot)

		# custom signal and widget
		self.logSignal.connect(self.logTextSlot)
		self.centerWin.editDict['addr'].focusOut.connect(lambda:self.addThread(self.focusOutSlot))
		for key in gSignalDict: gSignalDict[key][0].connect(gSignalDict[key][1])

	def _addSignalDict(self):
		'''
		registe all signal and slot function to gSignalDict
		'''
		gSignalDict['progress'] = (self.progressSignal, self.centerWin.progressBar.setValue)
		gSignalDict['txtfile']  = (self.txtfileEditSignal, self.centerWin.editDict['txtfile'].setText)
		gSignalDict['ramfile']  = (self.ramfileEditSignal, self.centerWin.editDict['ramfile'].setText)
		gSignalDict['romfile']  = (self.romfileEditSignal, self.centerWin.editDict['romfile'].setText)
		gSignalDict['otpfile']  = (self.otpfileEditSignal, self.centerWin.editDict['otpfile'].setText)
		gSignalDict['txtopen']  = (self.txtOpenSignal, self.txtOpenSlot)
		gSignalDict['ramopen']  = (self.ramOpenSignal, self.ramOpenSlot)
		gSignalDict['romopen']  = (self.romOpenSignal, self.romOpenSlot)
		gSignalDict['otpopen']  = (self.otpOpenSignal, self.otpOpenSlot)
		gSignalDict['rid'] 		= (self.ridUDSignal, lambda x,y='rid',z=gSccbLineEditNames:self.idUDSlot(y,z,x))
		gSignalDict['wid'] 		= (self.widUDSignal, lambda x,y='wid',z=gSccbLineEditNames:self.idUDSlot(y,z,x))
		gSignalDict['addr'] 	= (self.addrUDSignal, self.addrUDSlot)
		gSignalDict['data'] 	= (self.dataUDSignal, self.dataUDSlot)
		gSignalDict['fdfe']		= (self.fdfeAddrUDSignal, lambda x,y='fdfe',z=gSccbLineEditNames:self.emblUDSlot(y,z,x))
		gSignalDict['itemLock'] = (self.itemsLockSignal, self.centerWin.lockAllWidget)
		gSignalDict['fdfeLock'] = (self.fdfeLockSignal, self.centerWin.fdfeLockWidget)
		gSignalDict['sendfile'] = (self.sendFileSignal, self.snrOpenSlot)
		gSignalDict['sendButton']= (self.sendFileButtonSignal, self.sendFileBTSlot)
		gSignalDict['ramButton'] = (self.ramOpenButtonSignal, self.ramopenButtonSlot)
		gSignalDict['romButton'] = (self.romOpenButtonSignal, self.romopenButtonSlot)
		gSignalDict['txtButton'] = (self.txtOpenButtonSignal, self.txtopenButtonSlot)
		gSignalDict['otpButton'] = (self.otpOpenButtonSignal, self.otpopenButtonSlot)
		gSignalDict['start0'] =  (self.emblStartUDSignal, lambda x,y='start0',z=gEmblLineEditNames:self.emblUDSlot(y,z,x))
		gSignalDict['start1'] =  (self.emblStartUDSignal, lambda x,y='start1',z=gEmblLineEditNames:self.emblUDSlot(y,z,x))
		gSignalDict['len0']   =  (self.emblLenUDSignal,   lambda x,y='len0',z=gEmblLineEditNames:self.emblUDSlot(y,z,x))
		gSignalDict['len1']   =  (self.emblLenUDSignal,   lambda x,y='len1',z=gEmblLineEditNames:self.emblUDSlot(y,z,x))


##################################################################
# slot function for button
##################################################################
    # virtural function
	def txtopenButtonSlot(self, fileName):
		self.logPrint(self.LOG_DEBUG, "txt open button")

	def ramopenButtonSlot(self, fileName):
		self.logPrint(self.LOG_DEBUG, "ram open button")

	def romopenButtonSlot(self, fileName):
		self.logPrint(self.LOG_DEBUG, "rom open button")

	def otpopenButtonSlot(self, fileName):
		self.logPrint(self.LOG_DEBUG, "otp open button")

    # virtural function
	def reloadButtonSlot(self):
		self.logPrint(self.LOG_DEBUG, "reload button")

    # virtural function
	def downloadButtonSlot(self):
		self.logPrint(self.LOG_DEBUG, "download button")
		self.signalEmit('itemLock', True)
		tm.sleep(10)
		self.signalEmit('itemLock', False)

	def otpstartButtonSlot(self):
		self.logPrint(self.LOG_DEBUG, "otp start button")
		self.signalEmit('itemLock', True)
		tm.sleep(10)
		self.signalEmit('itemLock', False)

	def setupAboutUI(self):
		self.aboutWin =  UI_about()

	def mulitReadBTSlot(self):
		self.logPrint(self.LOG_DEBUG, "multi read button")

	def sendFileBTSlot(self, fileName):
		self.logPrint(self.LOG_DEBUG, "send file button")

	def emblShowSlot(self, lstart, vldbytes):
		self.logPrint(self.LOG_INFO, "show embl button")

##################################################################
# use for updating widget
##################################################################
	def signalEmit(self, idx, signalStr):
		gSignalDict[idx][0].emit(signalStr)

	def setLineEditTxt(self, idx, ctxStr):
		self.centerWin.editDict[idx].setText(ctxStr)
		if idx=='data': self.centerWin.editDict['data'].selectAll()

	def logPrint(self, logLv, logStr):
		if logLv <= self.logLvIdx+1:
			self.logSignal.emit((logLv,logStr))

	def logTextSlot(self, logTuple):
		if logTuple[0]==self.LOG_ERROR or logTuple[0]==self.LOG_FATAL:
			self.centerWin.logTextEdit.setTextColor(QColor('red'))
		if logTuple[0]==self.LOG_WARNING:
			self.centerWin.logTextEdit.setTextColor(QColor('darkRed'))
		self.centerWin.logTextEdit.append(gLogDist[logTuple[0]]+logTuple[1])
		self.centerWin.logTextEdit.setTextColor(QColor('black'))

	def imgClearup(self):
		if os.path.exists("./Data"):
			filelist = os.listdir("./Data")
			for fname in filelist:
				os.remove("./Data/"+fname)


##################################################################
# monitor input widget
###################################################################
	def getCheckValue(self, checkKey):
		setattr(self, gAllCheckNames[checkKey][1], int(self.centerWin.checkDict[checkKey].isChecked()))
#		print(checkKey, int(self.centerWin.checkDict[checkKey].isChecked()))

	def getEmblCheck(self, varDict, checkKey):
		varDict[checkKey[-1]] = int(self.centerWin.checkDict[checkKey].isChecked())
#		print(varDict, checkKey, varDict[checkKey[-1]])

	def getCombValue(self, item, valStr):
		setattr(self, valStr, item.currentIndex())
#		print(valStr, item.currentIndex())

	def devComboSlot(self):
		self.devIdx = self.centerWin.comboDict['dev'].currentIndex()

	def addrCombSlot(self):
		self.addrWidthIdx = self.centerWin.comboDict['addrwid'].currentIndex()
		addrRegExp = QRegExp()
		if self.addrWidthIdx == 0:
			addrRegExp.setPattern('[0-9a-fA-F]{,4}')
			if self.rAddr != -1:
				self.setLineEditTxt('addr', "{:X}".format(self.rAddr&0xffff))
		else:
			addrRegExp.setPattern('[0-9a-fA-F]{,8}')
		self.centerWin.editDict['addr'].setValidator(QRegExpValidator(addrRegExp))

	def dataCombSlot(self):
		self.dataWidthIdx = self.centerWin.comboDict['datawid'].currentIndex()
		dataRegExp, datStr = QRegExp(), self.centerWin.editDict['data'].text()
		if self.dataWidthIdx == 0:
			dataRegExp.setPattern('[0-9a-fA-F]{,2}')
			datStr = Util.getVldStr(datStr, 2, self.endianMode)
		elif self.dataWidthIdx == 1:
			dataRegExp.setPattern('[0-9a-fA-F]{,4}')
			datStr = Util.getVldStr(datStr, 4, self.endianMode)
		else:
			dataRegExp.setPattern('[0-9a-fA-F]{,8}')
		self.centerWin.editDict['data'].setValidator(QRegExpValidator(dataRegExp))
		self.centerWin.editDict['data'].setText(datStr)

	def fileNameSlot(self, fileName):
		if self.sender() == gSignalDict['txtfile'][0]:
			self.txtFileName = fileName
		if self.sender() == gSignalDict['ramfile'][0]:
			self.ramFileName = fileName
		if self.sender() == gSignalDict['romfile'][0]:
			self.romFileName = fileName
		if self.sender() == gSignalDict['otpfile'][0]:
			self.otpFileName = fileName

	def txtChangedSlot(self, valStr, datStr):
		'''
		update object value real time when lianEdit text changed
		'''
		if type(valStr) == type(''):
			setattr(self, valStr, int(datStr, 16) if datStr != '' else -1)
		elif type(valStr) == type((0,1)):
			valDict = getattr(self, valStr[0])
			valDict[valStr[1]] = int(datStr, 16) if datStr != '' else -1
#		print(valStr, datStr)

########################################################
# set lineEdit word upper
#######################################################
	def editUpperSlot(self, idx, dataStr):
		curCursor = self.centerWin.editDict[idx].cursorPosition()
		self.centerWin.editDict[idx].setText(dataStr.upper())
		self.centerWin.editDict[idx].setCursorPosition(curCursor)

	def focusOutSlot(self):
		self.logPrint(self.LOG_DEBUG, "sccb read data")

	def dataLineEnter(self):
		self.logPrint(self.LOG_DEBUG, "sccb write data")

	def fdfeLineEnter(self):
		self.logPrint(self.LOG_DEBUG, "fdfe write addr")

########################################################
# set keyboard event
#######################################################
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		if event.key() == Qt.Key_Up:
			self.signalEmit(getDictKey(self.focusWidget(), self.centerWin.editDict), 'up')
		if event.key() == Qt.Key_Down:
			self.signalEmit(getDictKey(self.focusWidget(), self.centerWin.editDict), 'down')

#	def keyReleaseEvent(self, event):
#		if QApplication.keyboardModifiers() == Qt.ShiftModifier:
#			if event.key() == Qt.Key_Tab:
#				self.logPrint(1, "tab press")
#			else:
#				self.logPrint(1, "shift release")

##################################################################
# line edit key signal slot
##################################################################
	def idUDSlot(self, editKey, keyDict, keyState):
		tmpVar = getattr(self, keyDict[editKey])
		if keyState == "up":
			if tmpVar == -1:
				self.setLineEditTxt(editKey, "0")
			else:
				self.setLineEditTxt(editKey, "{:X}".format((tmpVar+2)&0xff))
		else:
			if tmpVar == -1:
				self.setLineEditTxt(editKey, "{:X}".format(0xff))
			else:
				self.setLineEditTxt(editKey, "{:X}".format((tmpVar-2)&0xff))

	def addrUDSlot(self, keyState):
		maskNum = {0:0xffff, 1:0xffffffff}[self.addrWidthIdx]
		addrStep = 2**self.dataWidthIdx
		if keyState == "up":
			if self.rAddr == -1:
				self.setLineEditTxt('addr', "0")
			else:
				self.setLineEditTxt('addr', "{:X}".format((self.rAddr+addrStep)&maskNum))
		else:
			if self.rAddr == -1:
				self.setLineEditTxt('addr', "{:X}".format(maskNum))
			else:
				self.setLineEditTxt('addr', "{:X}".format((self.rAddr-addrStep)&maskNum))

	def dataUDSlot(self, keyState):
		maskNum = {0:0xff, 1:0xffff, 2:0xffffffff}[self.dataWidthIdx]
		if keyState == "up":
			if self.rData == -1:
				self.setLineEditTxt('data',"0")
			else:
				self.setLineEditTxt('data', "{:X}".format((self.rData+1)&maskNum))
		else:
			if self.rData == -1:
				self.setLineEditTxt('data', "{:X}".format(maskNum))
			else:
				self.setLineEditTxt('data', "{:X}".format((self.rData-1)&maskNum))

	def emblUDSlot(self, editKey, keyDict, keyState):
		maskNum = 0xffff
		strDict, strKey = getattr(self, keyDict[editKey])
		if keyState == "up":
			if strDict[strKey] == -1:
				self.setLineEditTxt(editKey, "0")
			else:
				self.setLineEditTxt(editKey, "{:X}".format((strDict[strKey]+1)&maskNum))
		else:
			if strDict[strKey] == -1:
				self.setLineEditTxt(editKey, "{:X}".format(maskNum))
			else:
				self.setLineEditTxt(editKey, "{:X}".format((strDict[strKey]-1)&maskNum))

##################################################################
# open signal slot
##################################################################
	def ramOpenSlot(self, dirName):
		fileName = QFileDialog.getOpenFileName(self, "open a bin file", dirName, "Bin Files (*.bin *.BIN)")[0]
		gSignalDict['ramButton'][0].emit(fileName)

	def romOpenSlot(self, dirName):
		fileName = QFileDialog.getOpenFileName(self, "open a bin file", dirName, "Bin Files (*.bin *.BIN)")[0]
		gSignalDict['romButton'][0].emit(fileName)

	def txtOpenSlot(self, dirName):
		fileName = QFileDialog.getOpenFileName(self, "open a txt file", dirName,"Txt Files (*.txt *.TXT)")[0]
		gSignalDict['txtButton'][0].emit(fileName)

	def otpOpenSlot(self, dirName):
		fileName = QFileDialog.getOpenFileName(self, "open a bin file", dirName,"Txt Files (*.bin *.BIN)")[0]
		gSignalDict['otpButton'][0].emit(fileName)

	def snrOpenSlot(self, dirName):
		fileName = QFileDialog.getOpenFileName(self, "open snr setting", dirName,"Txt Files (*.txt *.TXT)")[0]
		gSignalDict['sendButton'][0].emit(fileName)

	def fdfeMapSlot(self):
		cmdStr = "MapStart" if self.centerWin.buttonDict['fdfemap'].isChecked() else "MapFinish"
		self.centerWin.buttonDict['fdfemap'].setText(cmdStr)

	def errShowSlot(self):
		print('err show button')

	def showImgSlot(self):
		print('show img !!')

	def addrDatPrint(self, addr, datList, logLv):
		if len(datList) != 0:
			totLen,tmpAddr,tmpIdx = len(datList),addr,0
			while totLen > 0:
				addrLen = 4 - tmpAddr % 4
				tmpLen  = min(addrLen, totLen)
				errDate = combBytes(datList[tmpIdx:tmpIdx+tmpLen])
				if errDate != 0:
					self.logPrint(logLv, (r'{:x} {:0>'+str(tmpLen*2)+r'x}').format(tmpAddr, errDate))
				tmpAddr += tmpLen
				tmpIdx  += tmpLen
				totLen  -= tmpLen
		return True


##################################################################
# internal function
##################################################################
	def addThread(self, func):
		self.slotThread.task = func
		self.slotThread.start()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	UI = QSlotMain()
	sys.exit(app.exec_())
