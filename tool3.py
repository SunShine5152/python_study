# -*- coding:utf-8 -*-
#OAX4k.py
from check import sccbCRC, CommunicatError
from CommunicationPort import IPTDev
import time as tm
from check.crcdef import Crcdef
from Util import hexList

MHZ = 1000000

class OAX4KOTP(object):
	def __init__(self):
		self.efuse0BaseAddr = 0x9000
		self.efuse1BaseAddr = 0x9080
		self.otpRate = 0

	def otpInit(self):
		self.write(0x8053, 0xc0)			# module release
		self.write(0x806b, 0x07)			# module clkon
		self.write(0x9404, 0x00)			# module power down

	def otpStatusCheck(self, idx=0):
		addr = self.efuse0BaseAddr+0x21 if idx==0 else self.efuse1BaseAddr+0x20
		ebit = 0x01 if idx==0 else 0x80
		dlycnt, ret = 20, True
		while dlycnt > 0:
			val, _ = self.read(addr)
			if _ and not (val & ebit):
				ret = True; break
			else:
				dlycnt -= 1; tm.sleep(0.001)
		return ret

	def otpTimingCtrl(self, idx=0):
		addr = self.efuse0BaseAddr+0x18 if idx==0 else self.efuse1BaseAddr+0x18
		pdCycle = (1045*24//1000) + 1
		psCycle = (69*24//1000) + 1
		trdCycle = (200*24//1000) + 1
		tpgmCycle = (12000*24//1000) + 1
		val = (tpgmCycle<<16) | (trdCycle<<11) | (psCycle<<7) | pdCycle
		self.burstWrite(addr, [(val>>(i*8)) & 0xff for i in range(4)] )

	def otpRead(self, addr, length, idx=0):
		ret, retlist, wlength = True, [], (length+3)//4
		if idx==0:
			rdataAddr = self.efuse0BaseAddr
			while wlength > 0 :
				tmplen = 4 if wlength>=4 else wlength
				self.burstWrite(rdataAddr+0x14, [0x40, addr&0xff, (addr>>8)&0xff, tmplen])
				self.burstWrite(rdataAddr, [ 0 for i in range(16)])
				self.write(rdataAddr+0x14, 0x48)			# read enable
				if self.otpStatusCheck(idx):
					for i in range(tmplen*4):
						val, _ = self.read(rdataAddr+i)
						if _: retlist.append(val)
						else:
							raise IOError("sccb read failed !")
					wlength -= tmplen
					addr    += tmplen
					self.otpRate += tmplen/(len(retlist)+wlength)
				else:
					raise TimeoutError("check {:s} otp status time out !".format(self.__NAME__))
			return retlist, Crcdef.crc16l(retlist, 0x8005, 0xffff, 0)
		else:
			rdataAddr = self.efuse1BaseAddr
			while wlength > 0 :
				tmplen = 4 if wlength>=4 else wlength
				self.burstWrite(rdataAddr+0x14, [0x10, addr&0xff, tmplen])
				self.burstWrite(rdataAddr, [ 0 for i in range(16)])
				self.write(rdataAddr+0x14, 0x14)			# read start
				if self.otpStatusCheck(idx):
					for i in range(tmplen*4):
						val, _ = self.read(rdataAddr+i)
						if _: retlist.append(val)
						else:
							raise IOError("sccb read failed !")
					wlength -= tmplen
					addr    += tmplen
				else:
					raise TimeoutError("check {:s} otp status time out !".format(self.__NAME__))
			return retlist, Crcdef.crc16l(retlist, 0x8005, 0xffff, 0)

	def otpWrite(self, addr, datlist, idx=0):
		tmpidx, ret, length  = 0, True, len(datlist)
		if idx==0:
			wdataAddr = self.efuse0BaseAddr
			while length > 0:
				tmplen = 16 if length>=16 else length
				self.burstWrite(wdataAddr+0x14, [0x40, addr&0xff, (addr>>8)&0xff, (tmplen+3)//4])
				_ = self.burstWrite(wdataAddr, datlist[tmpidx:tmpidx+tmplen])
				if _:
					print("w:0x{:x} 0x{:x} {}".format(wdataAddr, addr, hexList(datlist[tmpidx:tmpidx+tmplen])))
				else:
					raise IOError("sccb read failed !")
				self.write(wdataAddr+0x14, 0x41)				# write enable
				if self.otpStatusCheck(idx):
					length -= tmplen
					tmpidx += tmplen
					addr   += (tmplen+3)//4
				else:
					raise TimeoutError("check {:s} otp status time out !".format(self.__NAME__))
			return Crcdef.crc16l(datlist, 0x8005, 0xffff, 0)
		else:
			wdataAddr = self.efuse1BaseAddr
			while length > 0:
				tmplen = 16 if length>=16 else length
				self.burstWrite(wdataAddr+0x14, [0x10, addr&0xff, (tmplen+3)//4])
				_ = self.burstWrite(wdataAddr, datlist[tmpidx:tmpidx+tmplen])
				if _:
					print("w:0x{:x}->{}".format(wdataAddr, hexList(datlist[tmpidx:tmpidx+tmplen])))
				else:
					raise IOError("sccb read failed !")
				self.write(wdataAddr+0x14, 0x11)			# write enable
				if self.otpStatusCheck(idx):
					length -= tmplen
					tmpidx += tmplen
					addr   += (tmplen+3)//4
				else:
					raise TimeoutError("check {:s} otp status time out !".format(self.__NAME__))
			return Crcdef.crc16l(datlist, 0x8005, 0xffff, 0)


class OAX4Kboard(OAX4KOTP):
	__NAME__ = "OAX4k"
	def __init__(self):
		super(OAX4Kboard, self).__init__()
		self.dev = IPTDev()
		self.id = 0x48
		self.crcInitVal = 0xffff
		self.ramBaseAddr = 0x80180000
		self.romBaseAddr = 0x80100000
		self.ramSize = 0x4f000						# 384k
		self.romSize = 0x18000						# 96k
		self.sccbsBaseAddr = 0x9600

		self.mapBaseAddr = 0
		self.mapEndAddr = 0
		self.fdfeAddrH = 0x8020						# used for fdfe mapping
		self.mapcfg = 0x03

	def mapClear(self):
		self.mapBaseAddr = 0
		self.mapEndAddr = 0

	def write(self, addr, data):
		return self.dev.write(self.id, addr, data)

	def burstWrite(self, addr, data):
		return self.dev.burstWrite(self.id, addr, data)

	def read(self, addr):
		return self.dev.read(self.id, addr)

	def burstRead(self, addr, length):
		return self.dev.burstRead(self.id, addr, length)

	def connect(self, devNo=1):
		self.dev.open(devNo)
		return self.dev.detect()

	def disconnect(self):
		return self.dev.close()

	def regReset(self):
		ret = self.write(0x805d, 0xff)
		return self.write(0x805d, 0x00) and ret

	def boot(self, memSel):
		'''
		memSel 1:ram boot, 0:rom boot
		'''
		ret = self.write(0x8001, 0x09)
		return self.write(0x8005, 0x04 | memSel<<1) and ret

	def cpuSuspend(self):
		return self.write(0x8050, 0x1)

	def cpuRelease(self):
		return self.write(0x8050, 0x0)

	def unlock(self):
		return self.burstWrite(self.sccbsBaseAddr+0x1c0, [0, 0])

	def crcInit(self):
		ret = self.write(self.sccbsBaseAddr+0x6a, 0x07)
		return ret and self.write(self.sccbsBaseAddr+0x6a, 0x06)

	def getHWcrcValue(self):
		dat, flag = self.burstRead(self.sccbsBaseAddr+0x68, 2)
		return (((dat[1]&0xff)<<8 | dat[0]&0xff)&0xffff, True) if flag else (0xffff, False)

	def getSWcrcValue(self, initVal, sccbAddr, datList):
		return sccbCRC.ibm_burst(initVal, sccbAddr, datList)

	def switchBaseAddr(self, BaseAddr, Length):
		sccbAddr, remapFlag, ret = 0x00, 0, True
		if (0x80200000 <= BaseAddr <= 0x80210000-Length) or \
			(0x200000 <= BaseAddr <= 0x210000-Length) or \
				(0x0000 <= BaseAddr <= 0x10000-Length):
			sccbAddr = BaseAddr&0xffff
		# mem range, Length<0x4000
		elif self.mapBaseAddr <= BaseAddr <= self.mapEndAddr+1-Length:
			sccbAddr = BaseAddr - self.mapBaseAddr
		else:
			self.mapBaseAddr = BaseAddr
			self.mapEndAddr = BaseAddr + 0x3fff
			dat = [ (BaseAddr>>(i*8))&0xff for i in range(4) ] + [0xff, 0x7f]
			ret = self.burstWrite(self.sccbsBaseAddr+0x44, dat)# remapping
			remapFlag = 1
		return sccbAddr, remapFlag, ret

	def fdfeMapStart(self, id, addrH):
		self.mapcfg, flg = self.dev.read(id, self.sccbsBaseAddr+0x01)
		if flg and self.dev.write(id, self.sccbsBaseAddr+0x01, self.mapcfg | 0x8):
			self.mapcfg |= 0x8
			return True
		return False

	def fdfeMapExit(self):
		if self.write(self.sccbsBaseAddr+0x01, self.mapcfg & 0xf7):
			self.mapcfg &= 0xf7
			return True
		return False

	def fdfeWrite(self, id, addrH):
		ret0, ret1 = False, False
		if self.dev.write(id, 0xfffd, (addrH>>8)&0xff):
			self.fdfeAddrH = (self.fdfeAddrH&0xff) | (addrH&0xff00)
			ret0 =  True
		if self.dev.write(id, 0xfffe, addrH&0xff):
			self.fdfeAddrH = (self.fdfeAddrH&0xff00) | (addrH&0xff)
			ret1 =  True
		return ret0 and ret1

	def ramClean(self, startAddr, endAddr):
		tmpaddr, ret, length = startAddr, True, endAddr-startAddr
		while tmpaddr < endAddr:
			sccbAddr, flag, _ = self.switchBaseAddr(tmpaddr, 4)
			if self.burstWrite(sccbAddr, [0,0,0,0]):
				tmpaddr += 4
			else:
				ret = False;break
		return ret

	def setNoCrcAddr(self):
		return self.burstWrite(self.sccbsBaseAddr+0x6c, [0xff, 0xff, 0x6a, 0x96])# set noncrc addr

	def handShake(self):
		self.write(self.sccbsBaseAddr+0x1c4, 0x4c)
		expectVal = self.read(self.sccbsBaseAddr+0x1c4)
		if expectVal[0] == 0x4c and expectVal[1]:
			pass
		else:
			raise CommunicatError((expectVal[0],"sccb access error!!"))

	def communicateErrDec(self, errValue):
		if   errValue == 0xff:
			return "please turn on or reboot board, or check slave id !!\n"
		elif errValue == 0x05:
			return "please turn on or reboot GAIA board !!\n"
		elif errValue == 0x00:
			return "please check sccb pad initial voltage !!\n"
		elif errValue == -1:
			return "please turn on GAIA board !!\n"
		else:
			return "get except value from board 0x{:x} !!\n".format(errValue)