# -*- coding: utf-8 -*-
#4kBurnTool.py
import sys, os, traceback,platform, Util
import numpy as np, time as tm, struct as st
from CommunicationPort.emblMon import EmblineMon, gFmtDecode
from CommunicationPort.imgCvt import ImgCvt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from PyQt5.Qt import PYQT_VERSION_STR
from QUI.QSlot4K import QSlotMain
from QUI.QUIWin4K import gComboDictNames
from check import CrcError,CommunicatError,AlignError
from check.crcdef import Crcdef
from Board.OAX4K import OAX4Kboard
from Board.OtpDev import OtpDev
from Parsers.SystemSetting import DeSysSetting
from Parsers.SnrSetting import DeSnrSetting


#slot function
class burnTool(QSlotMain):
    __VERSION__ = "3.8"
    __NAME__ = "{:s}BurnTool".format(OAX4Kboard.__NAME__)
    __VERSIONLOG__ = """                    {:s}
Version:    {:s}
Date:       21/2/5
Python:     {:s}
PyQt:       {:s}
Update:
    1, support txt fmt:16/32+8,32+8/16/32
    2, setting align check
    3, support download crc check
    4, compatible with windows7/8/10 64bit
    5, save setting when close application
    6, support GAIA or Venus setting
    7, support remapping for multi read
    8, add reload button to fresh communication
    9, add download bin to OTP
    10, support Venus
    11, add embline monitor""".format(__NAME__, __VERSION__, platform.python_version(), PYQT_VERSION_STR)

    def __init__(self, board):
        super(burnTool, self).__init__()
        # platform information
        self.board = board
        self.cvt = ImgCvt()
        self.embl = EmblineMon(self.board.dev)
        self.setWindowTitle(self.__NAME__ + "-V" + self.__VERSION__)
        self.txtParse = DeSysSetting()
        self.snrParse = DeSnrSetting()
        self.settingPath = "4ksystemSettingv3_8.ini"
        self.initDftSetting()
        self.readSetting() if os.path.exists(self.settingPath) else self.writeSetting()
        self.setDftValue()
        self.fLogInfoTxt = 'logInfoTxt.txt'
        self.fLogInfoRam = 'logInfoRam.txt'
        self.fLogInfoRom = 'logInfoRom.txt'
        self.imgShowSignal.connect(self.cvt.show)

        if self.board.connect(self.devIdx+1):
            self.logPrint(self.LOG_INFO, "detect device success !")
        else:
            self.logPrint(self.LOG_WARNING, "detect device failed !")

    def initDftSetting(self):
        '''
        set default value for some essential param
        '''
        self.txtFileName = ""
        self.snrFileName = ""
        self.ramFileName = ""
        self.romFileName = ""
        self.otpFileName = ""
        self.ramfileSelected = 0
        self.romfileSelected = 0
        self.txtfileSelected = 0
        self.otpfileSelected = 0
        self.bootMode = 1
        self.endianMode = 1
        self.txtFmtIdx = 2
        self.rid = 0x48
        self.wid = self.board.id
        self.devIdx = 1
        self.otpdevIdx = 0
        self.efuseIdx = 0
        self.imgcrcen = 0
        self.memIdx = 1
        self.fmtIdx = 0
        self.tagen = 0
        self.imgSave = 0
        self.displayen = 0
        self.addrWidthIdx = 0
        self.dataWidthIdx = 0
        self.logLvIdx = 3
        self.dpIdx = 0
        self.mdIdx = 0
        self.vcno = 0
        self.ramDownRdy = 0
        self.romDownRdy = 0
        self.txtDownRdy = 0
        self.otpDownStatus = 0xff
        self.otpDownRdy = 0

    def writeSetting(self):
        '''
        write user UI setting to db file
        '''
        self.setting = QSettings(self.settingPath,QSettings.IniFormat)
        self.setting.setValue("ramFileName", self.ramFileName)
        self.setting.setValue("romFileName", self.romFileName)
        self.setting.setValue("txtFileName", self.txtFileName)
        self.setting.setValue("snrFileName", self.snrFileName)
        self.setting.setValue("otpFileName", self.otpFileName)
        self.setting.setValue("logLvIdx", str(self.logLvIdx))
        self.setting.setValue("bootMode", str(self.bootMode))
        self.setting.setValue("tagen", str(self.tagen))
        self.setting.setValue("imgSave", str(self.imgSave))
        self.setting.setValue("displayen", str(self.displayen))
        self.setting.setValue("endianMode", str(self.endianMode))
        self.setting.setValue("devIdx", str(self.devIdx))
        self.setting.setValue("memIdx", str(self.memIdx))
        self.setting.setValue("fmtIdx", str(self.fmtIdx))
        self.setting.setValue("dpIdx", str(self.dpIdx))
        self.setting.setValue("mdIdx", str(self.mdIdx))
        self.setting.setValue("otpdevIdx", str(self.otpdevIdx))
        self.setting.setValue("efuseIdx", str(self.efuseIdx))
        self.setting.setValue("addrWidthIdx", str(self.addrWidthIdx))
        self.setting.setValue("dataWidthIdx", str(self.dataWidthIdx))
        self.setting.setValue("rid", str(self.rid))
        self.setting.setValue("wid", str(self.wid))
        self.setting.setValue("otpDownStatus", str(self.otpDownStatus))
        self.setting.setValue("romfileSelected", str(self.romfileSelected))
        self.setting.setValue("ramfileSelected", str(self.ramfileSelected))
        self.setting.setValue("txtfileSelected", str(self.txtfileSelected))
        del self.setting

    def readSetting(self):
        '''
        read db file, and set those value to system param
        '''
        self.setting = QSettings(self.settingPath,QSettings.IniFormat)
        self.ramFileName = self.setting.value("ramFileName")
        self.romFileName = self.setting.value("romFileName")
        self.txtFileName = self.setting.value("txtFileName")
        self.snrFileName = self.setting.value("snrFileName")
        self.otpFileName = self.setting.value("otpFileName")
        self.logLvIdx = int(self.setting.value("logLvIdx"))
        self.bootMode = int(self.setting.value("bootMode"))
        self.tagen = int(self.setting.value("tagen"))
        self.imgSave = int(self.setting.value("imgSave"))
        self.displayen = int(self.setting.value("displayen"))
        self.endianMode = int(self.setting.value("endianMode"))
        self.devIdx = int(self.setting.value("devIdx"))
        self.memIdx = int(self.setting.value("memIdx"))
        self.fmtIdx = int(self.setting.value("fmtIdx"))
        self.dpIdx = int(self.setting.value("dpIdx"))
        self.mdIdx = int(self.setting.value("mdIdx"))
        self.otpdevIdx = int(self.setting.value("otpdevIdx"))
        self.efuseIdx = int(self.setting.value("efuseIdx"))
        self.addrWidthIdx = int(self.setting.value("addrWidthIdx"))
        self.dataWidthIdx = int(self.setting.value("dataWidthIdx"))
        self.rid = int(self.setting.value("rid"))
        self.wid = int(self.setting.value("wid"))
        self.otpDownStatus = int(self.setting.value("otpDownStatus"))
        self.romfileSelected = int(self.setting.value("romfileSelected"))
        self.ramfileSelected = int(self.setting.value("ramfileSelected"))
        self.txtfileSelected = int(self.setting.value("txtfileSelected"))

    def setDftValue(self):
        '''show those param to UI
        '''
        for key in gComboDictNames:
            self.centerWin.comboDict[key].setCurrentIndex(getattr(self, gComboDictNames[key]))
        self.centerWin.checkDict['endian'].setChecked(self.endianMode==1)
        self.centerWin.checkDict['autoBoot'].setChecked(self.bootMode==1)
        self.centerWin.checkDict['tagen'].setChecked(self.tagen==1)
        self.centerWin.checkDict['save'].setChecked(self.imgSave==1)
        self.centerWin.checkDict['display'].setChecked(self.displayen==1)
        self.setLineEditTxt('rid', "{:X}".format(self.rid if self.rid != -1 else self.board.id))
        self.setLineEditTxt('wid', "{:X}".format(self.wid if self.wid != -1 else self.board.id))
        self.signalEmit('ramfile', self.ramFileName)
        self.signalEmit('romfile', self.romFileName)
        self.signalEmit('txtfile', self.txtFileName)
        self.centerWin.checkDict['romfile'].setChecked(self.romfileSelected==1)
        self.centerWin.checkDict['ramfile'].setChecked(self.ramfileSelected==1)
        self.centerWin.checkDict['txtfile'].setChecked(self.txtfileSelected==1)

    def ramopenButtonSlot(self, fileName):
        '''
        slot function of ram open button
        read a bin file to memory
        '''
        self.signalEmit('progress', 0)
        if fileName.endswith(".bin") or fileName.endswith(".BIN"):
            self.ramFileName = fileName
            self.signalEmit('ramfile', self.ramFileName)
            self.logPrint(self.LOG_INFO, "file name: "+os.path.basename(self.ramFileName))
            pFile = open(self.ramFileName, 'rb')
            self.fContentRam = pFile.read()
            self.fLenRam = len(self.fContentRam)
            self.logPrint(self.LOG_INFO, "file size: 0x{:x}\n".format(self.fLenRam))
            pFile.close()
            self.ramDownRdy = 1
        elif self.ramFileName.endswith(".bin") or self.ramFileName.endswith(".BIN"):
            self.ramDownRdy = 1
        else:
            self.ramDownRdy = 0
            self.logPrint(self.LOG_WARNING, "path or file name error!!")

    def otpopenButtonSlot(self, fileName):
        '''
        slot function of otp open button
        read a bin file to memory
        '''
        self.signalEmit('progress', 0)
        if fileName.endswith(".bin") or fileName.endswith(".BIN"):
            self.otpFileName = fileName
            self.signalEmit('otpfile', self.otpFileName)
            self.logPrint(self.LOG_INFO, "file name: "+os.path.basename(self.otpFileName))
            pFile = open(self.otpFileName, 'rb')
            self.fContentOtp = pFile.read()
            self.fLenOtp = len(self.fContentOtp)
            self.logPrint(self.LOG_INFO, "file size: 0x{:x}\n".format(self.fLenOtp))
            pFile.close()
            if self.fLenOtp % 4:
                self.logPrint(self.LOG_WARNING, "otp length cannot be divided by 4")
            self.otpDownRdy = 1
        elif self.otpFileName.endswith(".bin") or self.otpFileName.endswith(".BIN"):
            self.otpDownRdy = 1
        else:
            self.otpDownRdy = 0
            self.logPrint(self.LOG_WARNING, "path or file name error!!")

    def romopenButtonSlot(self, fileName):
        '''
        slot function of ram open button
        read a bin file to memory
        '''
        self.signalEmit('progress', 0)
        if fileName.endswith(".bin") or fileName.endswith(".BIN"):
            self.romFileName = fileName
            self.signalEmit('romfile', self.romFileName)
            self.logPrint(self.LOG_INFO, "file name: "+os.path.basename(self.romFileName))
            pFile = open(self.romFileName, 'rb')
            self.fContentRom = pFile.read()
            self.fLenRom = len(self.fContentRom)
            self.logPrint(self.LOG_INFO, "file size: 0x{:x}\n".format(self.fLenRom))
            pFile.close()
            self.romDownRdy = 1
        elif self.romFileName.endswith(".bin") or self.romFileName.endswith(".BIN"):
            self.romDownRdy = 1
        else:
            self.romDownRdy = 0
            self.logPrint(self.LOG_WARNING, "path or file name error!!")

    def txtopenButtonSlot(self, fileName):
        '''
        slot function of txt open button
        read a system setting file to memory, and pre operation
        '''
        self.signalEmit('progress', 0)
        if fileName.endswith(".txt") or fileName.endswith(".TXT"):
            self.txtFileName = fileName
            self.signalEmit('txtfile', self.txtFileName)
            self.logPrint(self.LOG_INFO, "file name: "+os.path.basename(self.txtFileName))
            pFile = open(self.txtFileName, 'r', encoding = "ascii")
            try:
                self.txtParse.preOperation(pFile.read())
            except :
                self.logPrint(self.LOG_FATAL,"setting fmt error !!")
            else:
                self.logPrint(self.LOG_INFO,"txt file valid lines: {:d}".format(self.txtParse.vldLineNum))
                self.txtDownRdy = 1
            finally:
                pFile.close()
        elif self.txtFileName.endswith(".txt") or self.txtFileName.endswith(".TXT"):
            self.txtDownRdy = 1
        else:
            self.logPrint(self.LOG_WARNING, "get no file !!")
            self.txtDownRdy = 0

    def downloadBlock(self, crcInitVal, baseAddr, dataList, fLogTxt):
        '''
        download a bloak system setting to chip
        and crc check
        '''
        tmpBase, dataLen, tmpIdx, crcVal = baseAddr, len(dataList), 0, crcInitVal
        OneTmLen = 0x40 if self.logLvIdx+1==self.LOG_DEBUG else 0x4000
        while dataLen > 0:
            tmpLen = min(OneTmLen, dataLen)
            if self.txtFmtIdx == 0:
                sccbAddr, remapFlag = tmpBase&0xffff, 0
            else:
                sccbAddr, remapFlag, ret = self.board.switchBaseAddr(tmpBase, tmpLen)
                if ret == False:
                    self.logPrint(self.LOG_ERROR, 'switch addr failed !!')
                    return 0xffff, False
                if remapFlag == 1:
                    dat = [(tmpBase>>(i*8))&0xff for i in range(4)] + [0xff, 0x7f]
                    crcVal = self.board.getSWcrcValue(crcVal, self.board.sccbsBaseAddr+0x44, dat)
                else:
                    pass
            self.rate += tmpLen / self.txtParse.vldDataNum

            if self.board.burstWrite(sccbAddr, dataList[tmpIdx:tmpIdx+tmpLen]):
                if self.logLvIdx+1==self.LOG_DEBUG:
                    print('w: 0x{:x}->'.format(tmpBase), end='', file=fLogTxt)
                    print(dataList[tmpIdx:tmpIdx+tmpLen], file=fLogTxt)
                    print('r: 0x{:x}->'.format(tmpBase), end='', file=fLogTxt)
                    print(self.board.burstRead(sccbAddr, tmpLen), file=fLogTxt)
                    print('', file=fLogTxt)

                self.logPrint(self.LOG_INFO,"send 0x{:0>4x} {:>5d} bytes !!".format(tmpBase,tmpLen))
                self.signalEmit('progress', int(self.rate*100+0.5))
                crcVal = self.board.getSWcrcValue(crcVal, sccbAddr, dataList[tmpIdx:tmpIdx+tmpLen])
                tmpBase += tmpLen
                tmpIdx  += tmpLen
                dataLen -= tmpLen
            else:
                self.logPrint(self.LOG_ERROR, 'sccb write error !!')
                return 0xffff, False
        return crcVal, True

    def downloadSettingFile(self):
        '''
        download system setting to chip
        and update progressbar
        '''
        crcVal, self.rate = self.board.crcInitVal, 0
        self.signalEmit('progress', 0)
        if not self.board.crcInit():
            self.logPrint(self.LOG_ERROR, "crc init failed !")
            return

        try:
            idx2dlist,id2dlist,addr2dlist,data2dlist = self.txtParse.decode(self.txtFmtIdx==2, self.endianMode, self.wid)
        except AlignError as msg:
            self.logPrint(self.LOG_FATAL,"align err addr:0x{:s},data:0x{:s}".format(msg.arg[0],msg.arg[1]))
        except:
            print(traceback.format_exc())
            self.logPrint(self.LOG_FATAL, "setting fmt error !")
        else:
            fLogTxt = open(self.fLogInfoTxt, 'w', encoding='utf-8')
            print(tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime()), file=fLogTxt)
            for i in range(len(idx2dlist)):
                if id2dlist[i][0] != self.wid:
                    self.rate += len(id2dlist[i]) / self.txtParse.vldDataNum
                    for j in range(len(id2dlist[i])):
                        tmpid = id2dlist[i][j]
                        tmpaddr = addr2dlist[i][j][0]
                        addrwidth = addr2dlist[i][j][1]*8
                        tmpdat = data2dlist[i][j][0]
                        datawidth = data2dlist[i][j][1]*8
#                       print("0x{:x} addr 0x{:x} {} dat 0x{:x} {}".format(tmpid,tmpaddr,addrwidth,tmpdat,datawidth))
                        if self.board.dev.write(tmpid, tmpaddr, tmpdat, addrWidth=addrwidth, dataWidth=datawidth):
                            self.logPrint(self.LOG_INFO, "w: {:x} {:x} {:X}".format(tmpid, tmpaddr, tmpdat))
                        else:
                            self.logPrint(self.LOG_ERROR, "w: {:x} {:x} {:X} failed !".format(tmpid, tmpaddr, tmpdat))
                            fLogTxt.close();return
                    self.signalEmit('progress', int(self.rate*100+0.5))
                else:
                    for j in range(len(idx2dlist[i])-1):
                        crcVal, boolRet = self.downloadBlock(crcVal,addr2dlist[i][idx2dlist[i][j]],data2dlist[i][idx2dlist[i][j]:idx2dlist[i][j+1]], fLogTxt)
                        if not boolRet:
                            fLogTxt.close();return
                if i == len(idx2dlist)-1:
                    pass
                else:
                    tm.sleep(0.001*self.txtParse.delayTm[i])
                    self.logPrint(self.LOG_INFO,"delay {:d}ms !!".format(self.txtParse.delayTm[i]))
            hwCrcVal, flag = self.board.getHWcrcValue()
            fLogTxt.close()
            if self.devIdx==1:
                return
            if hwCrcVal == crcVal and flag:
                self.logPrint(self.LOG_INFO,"crc check 0x{:0>4x}: 0x{:0>4x} pass!!".format(crcVal,hwCrcVal))
            else:
                self.logPrint(self.LOG_ERROR,"crc check 0x{:0>4x}: 0x{:0>4x} fail!!".format(crcVal,hwCrcVal))
                raise CrcError("crc error !!")

    def downloadBinFile(self, memSel, dataList, pfLog):
        '''
        download bin file to chip
        '''
        baseAddr = self.board.ramBaseAddr if memSel==1 else self.board.romBaseAddr
        fLenBin = self.fLenRam if memSel==1 else self.fLenRom
        tmpBase, dataLen, tmpIdx, rate = baseAddr, len(dataList), 0, 0
        OneTmLen = 0x40 if self.logLvIdx+1==self.LOG_DEBUG else 0x4000
        self.signalEmit('progress', 0)
        self.board.crcInit()
        print(tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime()), file=pfLog)
        while dataLen > 0:
            tmpLen = min(OneTmLen, dataLen)
            rate, crcVal = rate + tmpLen/fLenBin, self.board.crcInitVal
            sccbAddr, remapFlag, ret = self.board.switchBaseAddr(tmpBase, tmpLen)
            if ret == False:
                self.logPrint(self.LOG_ERROR, 'switch addr failed !!');break
            if remapFlag == 1:
                dat = [(tmpBase>>(i*8))&0xff for i in range(4)] + [0xff, 0x7f]
                crcVal = self.board.getSWcrcValue(crcVal, self.board.sccbsBaseAddr+0x44, dat)
            else:
                pass
            if self.board.burstWrite(sccbAddr, dataList[tmpIdx:tmpIdx+tmpLen]):
                if self.logLvIdx+1==self.LOG_DEBUG:
                    print('w: 0x{:x}->'.format(tmpBase), end='', file=pfLog)
                    print(st.unpack('{:d}B'.format(tmpLen), dataList[tmpIdx:tmpIdx+tmpLen]), file=pfLog)
                    print('r: 0x{:x}->'.format(tmpBase), end='', file=pfLog)
                    print(self.board.burstRead(sccbAddr, tmpLen), file=pfLog)
                    print('', file=pfLog)
            else:
                self.logPrint(self.LOG_ERROR, 'sccb write error !!');break
            self.signalEmit('progress', int(rate*100+0.5))
            crcGetFromCal = self.board.getSWcrcValue(crcVal, sccbAddr, dataList[tmpIdx:tmpIdx+tmpLen])
            crcGetFrom4k, flag  = self.board.getHWcrcValue()

            if crcGetFromCal == crcGetFrom4k and flag:
                self.logPrint(self.LOG_INFO,"crc check 0x{:0>4x}: 0x{:0>4x} pass!!".format(crcGetFromCal,crcGetFrom4k))
            else:
                self.logPrint(self.LOG_ERROR,"crc check 0x{:0>4x}: 0x{:0>4x} error!!".format(crcGetFromCal, crcGetFrom4k))
                raise CrcError("crc error !!")
            tmpBase += tmpLen
            tmpIdx  += tmpLen
            dataLen -= tmpLen

    def downloadButtonSlot(self):
        '''
        the slot funciton of download push button
        '''
        self.signalEmit('itemLock', True)
        consuTime = 0
#       self.memBaseAddr = {1:self.board.ramBaseAddr, 0:self.board.romBaseAddr}[self.memIdx]
        if self.wid != -1:
            self.board.id = self.wid & 0xfe
        if self.txtfileSelected == 1 or self.ramfileSelected == 1 or self.romfileSelected == 1:
            self.board.dev.comTest()
            try:
                self.board.handShake()
            except CommunicatError as msg:
                self.logPrint(self.LOG_FATAL, msg.arg[1])
                self.logPrint(self.LOG_INFO, self.board.communicateErrDec(msg.arg[0]))
                self.signalEmit('itemLock', False)
                return

            self.board.mapClear()
            self.board.cpuSuspend()
            self.board.setNoCrcAddr()

            if self.txtfileSelected == 1:
                if self.txtDownRdy == 1:
                    try:
                        self.logPrint(self.LOG_INFO, "download setting start !!")
                        startTime = tm.time()
                        self.downloadSettingFile()
                        consuTime = tm.time() - startTime
                    except CrcError:
                        self.logPrint(self.LOG_FATAL, "crc error !!")
                        self.signalEmit('itemLock', False)
                        self.board.cpuRelease()
                        return
                    else:
                        self.logPrint(self.LOG_INFO, "download txt elapsed {:.2f}s!!".format(consuTime))
                else:
                    self.logPrint(self.LOG_WARNING, "txt file name error !!")
            else:
                pass

            if self.romfileSelected == 1:
                if self.romDownRdy == 1:
                    try:
                        self.logPrint(self.LOG_INFO, "download rom bin start !!")
                        startTime = tm.time()
                        pFile = open(self.fLogInfoRom, mode = 'w',encoding='utf-8')
                        self.downloadBinFile(0, self.fContentRom, pFile)
                        pFile.close()
                        consuTime = tm.time() - startTime
                    except CrcError:
                        self.logPrint(self.LOG_FATAL, "crc error !!")
                        self.signalEmit('itemLock', False)
                        self.board.cpuRelease()
                        return
                    else:
                        self.logPrint(self.LOG_INFO, "download rom bin elapsed {:.2f}s!!".format(consuTime))
                else: self.logPrint(self.LOG_WARNING, "rom bin file name error !!")

            if self.ramfileSelected == 1:
                if self.ramDownRdy == 1:
                    try:
                        self.logPrint(self.LOG_INFO, "download ram bin start !!")
                        startTime = tm.time()
                        pFile = open(self.fLogInfoRam, mode = 'w',encoding='utf-8')
                        self.downloadBinFile(1, self.fContentRam, pFile)
                        pFile.close()
                        consuTime = tm.time() - startTime
                    except CrcError:
                        self.logPrint(self.LOG_FATAL, "crc error !!")
                        self.signalEmit('itemLock', False)
                        self.board.cpuRelease()
                        return
                    else:
                        self.logPrint(self.LOG_INFO,"download ram bin elapsed {:.2f}s!!".format(consuTime))
                else: self.logPrint(self.LOG_WARNING, "ram bin file name error !!")
            else: pass

            if (self.ramfileSelected == 1 or self.romfileSelected == 1) and self.bootMode:
                if not self.board.boot(self.memIdx):
                    self.logPrint(self.LOG_FATAL, "boot failed !")
                self.board.cpuRelease()
        else:
            self.logPrint(self.LOG_WARNING, "none file selected !!")
        self.signalEmit('itemLock', False)

    def otpBurnOAX4K(self):
        self.board.otpInit()
        self.board.otpTimingCtrl(self.efuseIdx)
        try:
            retlistr, crcvalr = self.board.otpRead(0, 1984, self.efuseIdx)
        except IOError:
            self.logPrint(self.LOG_ERROR, 'sccb access error !');return
        except TimeoutError:
            self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(self.board.__NAME__));return
        except :
            self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
            print(traceback.format_exc());return
        else:
            if sum(retlistr) == 0:
                self.logPrint(self.LOG_INFO, "the first 1984bytes all zero !")
            else:
                filename = "Data/otp/"+"{:s}_{:d}_{:x}_".format(self.board.__NAME__, 1984, crcvalr)+tm.strftime("%Y%m%d_%H%M%S",tm.localtime())+'.bin'
                np.array(retlistr, np.uint8).tofile(filename)
                self.logPrint(self.LOG_INFO, "the first 1984bytes not zero ! 0x{:x}".format(crcvalr))

        if self.otpfileSelected and self.otpDownRdy:
            try:                                # download
                crcvalw = self.board.otpWrite(0, self.fContentOtp, self.efuseIdx)
            except IOError:
                self.logPrint(self.LOG_ERROR, 'sccb access error !');return
            except TimeoutError:
                self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(self.board.__NAME__));return
            except :
                self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
                print(traceback.format_exc());return
            else:
                self.logPrint(self.LOG_INFO, "otp write finished !")
                self.logPrint(self.LOG_INFO, "please wait to read back for check ...")

                try:
                    retlistr, crcvalr = self.board.otpRead(0, self.fLenOtp, self.efuseIdx)
                except IOError:
                    self.logPrint(self.LOG_ERROR, 'sccb access error !');return
                except TimeoutError:
                    self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(self.board.__NAME__));return
                except :
                    self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
                    print(traceback.format_exc());return
                else:
                    if crcvalr != crcvalw:
                        self.logPrint(self.LOG_ERROR, "0x{:x}: 0x{:x} failed !".format(crcvalw, crcvalr))
                    else:
                        self.logPrint(self.LOG_INFO, "0x{:x}: 0x{:x} pass !".format(crcvalw, crcvalr))
        else:
            self.logPrint(self.LOG_WARNING, "download not ready !")

    def otpBurnX8B(self, otpdev):
        try:
            lockStatus = otpdev.otpLockCheck()
        except IOError:
            self.logPrint(self.LOG_ERROR, 'sccb access error !');return
        except TimeoutError:
            self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(otpdev.__NAME__));return
        except :
            self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
            print(traceback.format_exc());return
        else:
            if lockStatus == 0x00:
                self.logPrint(self.LOG_INFO, "{:s} OTP is clean !".format(otpdev.__NAME__))
                self.otpDownStatus = 0
            elif lockStatus == 0xa5aaaaaa:
                self.logPrint(self.LOG_INFO, "{:s} OTP is unlocked !".format(otpdev.__NAME__))
                if self.otpDownStatus == 0xff:
                    self.otpDownStatus = 1
                else:
                    self.otpDownStatus += 1
            else:
                self.logPrint(self.LOG_INFO, "{:s} OTP lock status 0x{:x}".format(otpdev.__NAME__, lockStatus))
                self.otpDownStatus = 0xff
                return

        if self.otpfileSelected and self.otpDownRdy:
            if self.otpDownStatus == 0:
                try:
                    otpdev.otpWrite(0x11000, self.fContentOtp[0:4])
                except TimeoutError:
                    self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(otpdev.__NAME__));return
                except IOError:
                    self.logPrint(self.LOG_ERROR, 'sccb access error !');return
                except :
                    self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
                    print(traceback.format_exc()); return
                else:
                    self.logPrint(self.LOG_INFO, "OTP is unlocked, please restart device ...")
            elif self.otpDownStatus == 1:
                try:
                    otpdev.otpWrite(0x11004, self.fContentOtp[4:])
                except TimeoutError:
                    self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(otpdev.__NAME__));return
                except:
                    self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
                    print(traceback.format_exc());return
                else:
                    self.logPrint(self.LOG_INFO, "OTP burn finished, please restart device ...")
            elif self.otpDownStatus == 2:
                crcvalw = Crcdef.crc16l(self.fContentOtp, 0x8005, 0xffff, 0)
                try:
                    retlist, crcvalr = otpdev.otpRead(0x11000, 2048)
                except TimeoutError:
                    self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(otpdev.__NAME__));return
                except IOError:
                    self.logPrint(self.LOG_ERROR, 'sccb access error !');return
                except:
                    self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
                    print(traceback.format_exc());return
                else:
                    if crcvalr==crcvalw:
                        self.logPrint(self.LOG_INFO, "OTP read check 0x{:x}: 0x{:x} pass".format(crcvalw, crcvalr))
                    else:
                        self.logPrint(self.LOG_ERROR, "OTP read check 0x{:x}: 0x{:x} fail".format(crcvalw, crcvalr))
                    filename = "Data/otp/"+"{:s}_{:d}_{:x}_".format(otpdev.__NAME__, 2048, crcvalr)+tm.strftime("%Y%m%d_%H%M%S",tm.localtime())+'.bin'
                    np.array(retlist, np.uint8).tofile(filename)
                    self.otpDownStatus = 0xff
            else:
                self.logPrint(self.LOG_ERROR, "unrecognize OTP status !")
        else:
            if self.otpDownStatus == 1:
                try:
                    retlist, crcvalr = otpdev.otpRead(0x11000, 2048)
                except TimeoutError:
                    self.logPrint(self.LOG_ERROR, 'check {:s} status timeout !'.format(otpdev.__NAME__));return
                except IOError:
                    self.logPrint(self.LOG_ERROR, 'sccb access error !');return
                except:
                    self.logPrint(self.LOG_ERROR, 'some unrecognized exception occurred !')
                    print(traceback.format_exc());return
                else:
                    filename = "Data/otp/"+"{:s}_{:d}_{:x}_".format(otpdev.__NAME__, 2048, crcvalr)+tm.strftime("%Y%m%d_%H%M%S",tm.localtime())+'.bin'
                    np.array(retlist, np.uint8).tofile(filename)
                    self.logPrint(self.LOG_INFO, "check first 2048bytes crc 0x{:x}".format(crcvalr))
            else:
                self.logPrint(self.LOG_INFO, "download not ready !")


    def otpstartButtonSlot(self):
        '''
        slot function of otp start push button
        download otp binfile to otpdev
        '''
        self.signalEmit('itemLock', True)
        self.board.dev.comTest()

        otpdev = self.board if self.otpdevIdx==0 else OtpDev(self.board.dev)
        try:
            otpdev.handShake()
        except CommunicatError as msg:
            self.logPrint(self.LOG_FATAL, msg.arg[1])
            self.logPrint(self.LOG_INFO, self.board.communicateErrDec(msg.arg[0]))
            self.signalEmit('itemLock', False)
            return
        if os.path.exists('./Data/otp'): pass
        else: os.mkdir('./Data/otp')
        startTime = tm.time()
        if self.otpdevIdx==0: self.otpBurnOAX4K()
        else: self.otpBurnX8B(otpdev)
        consuTime = tm.time() - startTime
        self.logPrint(self.LOG_INFO, "download otp bin elapsed {:.2f}s!!".format(consuTime))
        self.signalEmit('itemLock', False)

    # reload file according check button
    def reloadButtonSlot(self):
        '''
        slot function of reload push button
        1, read bin file and setting file to ram
        2, device connect refresh
        '''
        self.signalEmit('progress', 0)
        txtFeditName = self.centerWin.editDict['txtfile'].text()
        ramFeditName = self.centerWin.editDict['ramfile'].text()
        romFeditName = self.centerWin.editDict['romfile'].text()
        otpFeditName = self.centerWin.editDict['otpfile'].text()
        # communication refresh
        if self.board.dev.comTest():
            self.logPrint(self.LOG_INFO, "communication refresh success !")
        else:
            self.logPrint(self.LOG_ERROR, "communication refresh failed !")

        self.otpDownStatus = int(self.setting.value("otpDownStatus"))
        if self.ramfileSelected == 0 and self.txtfileSelected == 0 and self.romfileSelected == 0 and self.otpfileSelected==0:
            self.logPrint(self.LOG_WARNING, "none file selected !!")
            return

        if self.ramfileSelected == 1:
            if os.path.isfile(ramFeditName):
                self.ramFileName = ramFeditName
                self.logPrint(self.LOG_INFO, "reload ram bin:" + os.path.basename(self.ramFileName))
                with open(self.ramFileName, 'rb') as pFile:
                    self.fContentRam = pFile.read()
                    self.fLenRam = len(self.fContentRam)
                    self.logPrint(self.LOG_INFO, "file size: 0x{:x}".format(self.fLenRam))
                    self.ramDownRdy = 1
            else:
                self.logPrint(self.LOG_WARNING, 'selected ram bin is not exist !')
                self.ramDownRdy = 0
                return

        if self.romfileSelected == 1:
            if os.path.isfile(romFeditName):
                self.romFileName = romFeditName
                self.logPrint(self.LOG_INFO, "reload rom bin:" + os.path.basename(self.romFileName))
                with open(self.romFileName, 'rb') as pFile:
                    self.fContentRom = pFile.read()
                    self.fLenRom = len(self.fContentRom)
                    self.logPrint(self.LOG_INFO, "file size: 0x{:x}".format(self.fLenRom))
                    self.romDownRdy = 1
            else:
                self.logPrint(self.LOG_WARNING, 'selected rom bin is not exist !')
                self.romDownRdy = 0
                return

        if self.otpfileSelected == 1:
            if os.path.isfile(otpFeditName):
                self.otpFileName = otpFeditName
                self.logPrint(self.LOG_INFO, "reload otp bin:" + os.path.basename(self.otpFileName))
                with open(self.otpFileName, 'rb') as pFile:
                    self.fContentOtp = pFile.read()
                    self.fLenOtp = len(self.fContentOtp)
                    self.logPrint(self.LOG_INFO, "file size: 0x{:x}".format(self.fLenOtp))
                    self.otpDownRdy = 1
                    if self.fLenOtp % 4:
                        self.logPrint(self.LOG_WARNING, "otp length cannot be divided by 4 !")
            else:
                self.logPrint(self.LOG_WARNING, 'selected otp bin is not exist !')
                self.otpDownRdy = 0
                return

        if self.txtfileSelected == 1:
            if os.path.isfile(txtFeditName):
                self.txtFileName = txtFeditName
                self.logPrint(self.LOG_INFO,"reload setting file:" + os.path.basename(self.txtFileName))
                with open(self.txtFileName, 'r', encoding = "ascii") as pFile:
                    self.txtParse.preOperation(pFile.read())
                    self.logPrint(self.LOG_INFO,"txt file valid lines: {:d}".format(self.txtParse.vldLineNum))
                    self.txtDownRdy = 1
            else:
                self.logPrint(self.LOG_WARNING, "selected txt file is not exist !")
                self.txtDownRdy = 0
                return


    def focusOutSlot(self):
        '''use tab key to show data read from chip
        '''
        dataWidth, rdat, addrWidth = 2**self.dataWidthIdx, 0, 16*(self.addrWidthIdx+1)
#       print("{}".format(addrWidth))
        if self.rid != -1 and self.rAddr != -1 and self.focusWidget() == self.centerWin.editDict['data']:
            datList, flag = [], True
            if self.devIdx==1 and self.rid==0x64:
                rdat, flag = self.board.dev.read(self.rid, self.rAddr, addrWidth=addrWidth, dataWidth=dataWidth*8)
                if self.endianMode==0:
                    rdat = Util.endianSwap(rdat, 4)
            elif self.devIdx==1:
                for i in range(dataWidth):
                    ret, _ = self.board.dev.read(self.rid, self.rAddr+i, addrWidth=addrWidth)
                    datList.append(ret)
                    flag = flag and _
                if flag:
                    rdat = Util.combDat(datList, dataWidth, self.endianMode)
            else:
                datList, flag = self.board.dev.burstRead(self.rid, self.rAddr, dataWidth, addrWidth=addrWidth)
                if flag:
                    rdat = Util.combDat(datList, dataWidth, self.endianMode)
            if flag:
                self.setLineEditTxt('data', (r"{:0>"+str(2*dataWidth)+r"X}").format(rdat))
                self.logPrint(self.LOG_INFO, (r"R: {:0>2X} {:0>4X} {:0>"+str(2*dataWidth)+r"X}").format(self.rid, self.rAddr, rdat))
            else:
                self.logPrint(self.LOG_ERROR, "sccb read failed !")
                rdat = int('ff'*dataWidth, 16)
                self.setLineEditTxt('data', "{:0>2X}".format(rdat))
        else: pass

    def dataLineEnter(self):
        '''
        use enter key to write data to chip
        '''
        dataWidth = 2**self.dataWidthIdx
        if self.rid != -1 and self.rAddr != -1 and self.rData != -1 :
            if self.devIdx==1 and self.rid == 0x64:
                flag = self.board.dev.write(self.rid, self.rAddr, self.rData, addrWidth=32)
            else:
                wdat = Util.splitDat(self.rData, dataWidth, self.endianMode)
                flag = self.board.dev.burstWrite(self.rid, self.rAddr, wdat)
            if flag:
                self.logPrint(self.LOG_INFO, (r"W: {:0>2X} {:0>4X} {:0>"+str(2*dataWidth)+r"X}").format(self.rid, self.rAddr, self.rData))
            else:
                self.logPrint(self.LOG_ERROR, "sccb write failed !")
        else: pass

    def fdfeLineEnter(self):
        '''
        write fdfe mapping high addr to chip
        '''
        if self.fdfeAddr!=-1 and (self.board.mapcfg & 0x8) and self.rid != -1:
            if self.board.fdfeWrite(self.rid, self.fdfeAddr):
                self.logPrint(self.LOG_INFO, "fdfe mapping to 0x{:X}".format(self.board.fdfeAddrH))
            else:
                self.logPrint(self.LOG_ERROR, "fdfe mapping to 0x{:X}".format(self.board.fdfeAddrH))
        else:
            self.logPrint(self.LOG_ERROR, "lack necessary param ")


    def mulitReadBTSlot(self):
        dataWidth = 2**self.dataWidthIdx
        if self.rid != -1 and self.rAddr != -1 and self.rData != -1 and self.rData != 0:
            self.signalEmit('itemLock', True)
            rLength = dataWidth * self.rData
            rdat, flag = [], True
            if self.devIdx==0:
                rdat, flag = self.board.dev.burstRead(self.rid, self.rAddr, rLength,addrWidth=16*(self.addrWidthIdx+1))
            else:
                for i in range(rLength):
                    ret, _ = self.board.dev.read(self.rid, self.rAddr+i, addrWidth=16*(self.addrWidthIdx+1))
                    rdat.append(ret)
                    flag = flag and _
            if flag:
                for i in range(self.rData):
                    tmpDat = Util.combDat(rdat[i*dataWidth:(i+1)*dataWidth], dataWidth, self.endianMode)
                    self.logPrint(self.LOG_INFO, (r"R: {:0>2X} {:0>4X} {:0>"+str(2*dataWidth)+r"X}").format(self.rid, self.rAddr+i*dataWidth, tmpDat))
            else:
                self.logPrint(self.LOG_ERROR, "sccb read failed !")
            self.signalEmit('itemLock', False)
        else:
            self.logPrint(self.LOG_ERROR, "no addr or data")

    def sendFileBTSlot(self, fileName):
        '''
        slot function of send file push button
        download snr setting to chip
        '''
        self.signalEmit('progress', 0)
#       fileName = QFileDialog.getOpenFileName(self, "open snr setting", os.path.dirname(self.snrFileName),"Txt Files (*.txt)")[0]
        if fileName.endswith(".txt") or fileName.endswith(".TXT"):
            self.snrFileName = fileName
            pFile = open(self.snrFileName, 'r', encoding = "ascii")
            try:
                self.snrParse.preOperation(pFile.read(), self.devIdx==0)
            except:
                self.logPrint(self.LOG_FATAL, "setting fmt error !")
            else:
                self.addThread(self.downSnrSetting)
            finally:
                pFile.close()

    def downSnrSetting(self):
        self.rate, consuTime = 0, 0
        try:
            startTime = tm.time()
            idx2dlist, id2dlist, addr2dlist, data2dlist = self.snrParse.decode()
            for i in range(len(idx2dlist)):
                for j in range(len(idx2dlist[i])-1):
                    if addr2dlist[i][idx2dlist[i][j]][1] == 16:
                        if self.board.dev.burstWrite(id2dlist[i][idx2dlist[i][j]],
                                                addr2dlist[i][idx2dlist[i][j]][0],
                                                    data2dlist[i][idx2dlist[i][j]:idx2dlist[i][j+1]],
                                                        addrWidth=addr2dlist[i][idx2dlist[i][j]][1],
                                                            dataWidth=addr2dlist[i][idx2dlist[i][j]][2]):
                            for k in range(idx2dlist[i][j+1] - idx2dlist[i][j]):
                                self.logPrint(self.LOG_INFO, "W: {:0>2X} {:0>4X} {:0>2X}".format(id2dlist[i][idx2dlist[i][j]+k],
                                                addr2dlist[i][idx2dlist[i][j]+k][0],
                                                    data2dlist[i][idx2dlist[i][j]+k]))

                            self.rate += (idx2dlist[i][j+1] - idx2dlist[i][j]) / self.snrParse.vldLineNum
                            self.signalEmit('progress', int(self.rate*100+0.5))
                        else:
                            self.logPrint(self.LOG_ERROR, "sccb write failed !")
                            raise CommunicatError
                    else:
                        for k in range(idx2dlist[i][j+1]-idx2dlist[i][j]):
                            if self.board.dev.write(id2dlist[i][idx2dlist[i][j]],
                                                addr2dlist[i][idx2dlist[i][j]][0],
                                                    data2dlist[i][idx2dlist[i][j]+k],
                                                        addrWidth=addr2dlist[i][idx2dlist[i][j]][1],
                                                            dataWidth=addr2dlist[i][idx2dlist[i][j]][2]):
                                self.logPrint(self.LOG_INFO, "W: {:0>2X} {:0>4X} {:0>2X}".format(id2dlist[i][idx2dlist[i][j]+k],
                                                                                        addr2dlist[i][idx2dlist[i][j]+k][0],
                                                                                            data2dlist[i][idx2dlist[i][j]+k]))
                            else:
                                self.logPrint(self.LOG_ERROR, "sccb write failed !")
                                raise CommunicatError
                        self.rate += (idx2dlist[i][j+1] - idx2dlist[i][j]) / self.snrParse.vldLineNum
                        self.signalEmit('progress', int(self.rate*100+0.5))
                if i == len(idx2dlist)-1:
                    pass
                else:
                    tm.sleep(self.snrParse.delayTm[i]*0.001)
                    self.logPrint(self.LOG_INFO, "delay {:d}ms !!".format(self.snrParse.delayTm[i]))
            consuTime = tm.time() - startTime
        except :
            print(traceback.format_exc())
            self.logPrint(self.LOG_FATAL, "setting fmt error !")
        else:
            self.logPrint(self.LOG_INFO, "download snr txt elapsed {:.2f}s ".format(consuTime))
        finally:
            pass
#           self.signalEmit('itemLock', False)

    def fdfeMapSlot(self):
        if self.centerWin.buttonDict['fdfemap'].isChecked():
            self.tmpAddrWidth = self.addrWidthIdx
            self.centerWin.comboDict['addrwid'].setCurrentIndex(0)
            self.signalEmit('fdfeLock', True)
            self.centerWin.buttonDict['fdfemap'].setText("ExitFeMode")
            if self.board.fdfeMapStart(self.rid, self.fdfeAddr):
                self.logPrint(self.LOG_INFO, "set FDFE map mode success !!")
            else:
                self.logPrint(self.LOG_ERROR, "set FDFE map mode failed !!")
        else:
            self.centerWin.buttonDict['fdfemap'].setText("SetFeMode")
            self.board.fdfeWrite(self.rid, 0x8020)
            if self.board.fdfeMapExit():
                self.logPrint(self.LOG_INFO, "exit FDFE map mode success !!")
            else:
                self.logPrint(self.LOG_ERROR, "exit FDFE map mode failed !!")
            self.signalEmit('fdfeLock', False)
            self.centerWin.comboDict['addrwid'].setCurrentIndex(self.tmpAddrWidth)

    def devComboSlot(self):
        '''
        switch device, GAIA or Venus
        '''
        super().devComboSlot()
        self.board.disconnect()
        if self.board.connect(self.devIdx+1):
            self.logPrint(self.LOG_INFO, "device open success")
        else:
            self.logPrint(self.LOG_ERROR, "device open failed")

    # show version information
    def setupAboutUI(self):
        super().setupAboutUI()
        self.aboutWin.display(self.__VERSIONLOG__)


    def emblShowSlot(self):
        if sum(self.emblSel.values())==0:
            self.logPrint(self.LOG_WARNING, 'none selected !')
        else:
            self.signalEmit('itemLock', True)
            if self.embl.devInit():
                self.embl.tagen = self.tagen
                self.embl.save = self.imgSave
                if self.devIdx==0:
                    ret, _ = self.embl.getGaiaEmbl(16)
                    if not _: self.logPrint(self.LOG_ERROR, ret)
                else:
                    self.embl.setSize(self.fmtIdx, self.vcno, self.imgHsize, self.imgVsize)
                if self.embl.getImg(16, self.devIdx):
                    self.logPrint(self.LOG_INFO, 'hsize 0x{:x}, vsize 0x{:x}'.format(self.embl.hsize, self.embl.vsize))
                    self.logPrint(self.LOG_INFO, 'vc{:0}, fmt {:s}'.format(self.embl.vcno, gFmtDecode[self.embl.dataType]))
                    self.logPrint(self.LOG_INFO, 'embline show start !')
                    for key in '01':
                        if self.emblSel[key]==0 or self.emblStart[key]==-1 or self.emblLen[key]==-1:
                            pass
                        else:
                            try:
                                retEmbl, crcval, calval = self.embl.getEmbl(self.emblStart[key], self.emblLen[key])
                            except:
                                print(traceback.format_exc())
                                self.logPrint(self.LOG_ERROR, traceback.format_exc())
                                self.signalEmit('itemLock', False)
                                return
                            self.logPrint(self.LOG_NONE, Util.listToStr(retEmbl, 16))
                            if crcval == calval:
                                self.logPrint(self.LOG_INFO, 'crc 0x{:0>8x}:0x{:0>8x} pass'.format(crcval, calval))
                            else: self.logPrint(self.LOG_INFO, 'crc 0x{:0>8x}:0x{:0>8x} fail'.format(crcval, calval))
                    if self.imgcrcen==1:
                        hwcrc, swcrc = self.embl.getImgCrc()
                        if hwcrc==swcrc:
                            self.logPrint(self.LOG_INFO, 'img crc 0x{:0>8x}:0x{:0>8x} pass'.format(hwcrc, swcrc))
                        else:
                            self.logPrint(self.LOG_ERROR, 'img crc 0x{:0>8x}:0x{:0>8x} fail'.format(hwcrc, swcrc))
                    if self.displayen:
                        self.imgShowSignal.emit((self.embl.extOrigDat(), self.embl.dataType,self.vcno))
                else: self.logPrint(self.LOG_ERROR, 'get image data failed !')

            else: self.logPrint(self.LOG_ERROR, "communication error !!")
            self.signalEmit('itemLock', False)

    # close UI and save setting
    def closeEvent(self,event):
        '''
        callback function when close app
        1, save setting file
        2, disconnect device
        3, close app
        '''
        self.writeSetting()
        self.board.disconnect()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tool = burnTool(OAX4Kboard())
    print('***ace 000***')
    sys.exit(app.exec_())