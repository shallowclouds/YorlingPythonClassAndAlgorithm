#coding=utf-8
import RPi.GPIO as GPIO
import time
import threading
class Nums:
	ledPos={"anodeL":11,"anodeR":12,"LA":16,"LB":18,"LC":21,"LD":22,"LE":15,"LF":19,"LG":13}
	portList=[11,12,13,16,15,18,19,21,22]
	numList=[13,16,15,18,19,21,22]
	numConst={
		0:["LA","LB","LC","LF","LG","LE"],
		1:["LC","LF"],
		2:["LB","LC","LD","LE","LG"],
		3:["LB","LC","LD","LF","LG"],
		4:["LA","LD","LC","LF"],
		5:["LB","LA","LD","LF","LG"],
		6:["LB","LA","LE","LD","LF","LG"],
		7:["LB","LC","LF"],
		8:["LA","LB","LC","LD","LE","LG","LF"],
		9:["LA","LB","LC","LD","LF","LG"],}
	cLock=threading.Lock()
	isStop=False
	Lnum=0
	Rnum=0
	disThreading=None
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		for i in self.portList:
			GPIO.setup(i,GPIO.OUT)
		for i in self.numList:
			GPIO.output(i,True)
		GPIO.output(self.ledPos["anodeL"],False)
		GPIO.output(self.ledPos["anodeR"],False)
		GPIO.setwarnings(False)
		print("Class Nums init successfully.")
		self.disThreading=threading.Thread(target=self.displayThreading)
		self.disThreading.setDaemon(True)
		self.disThreading.start()
	def cleanPrev(self):
		for i in self.numList:
			GPIO.output(i,True)
		GPIO.output(self.ledPos["anodeL"],False)
		GPIO.output(self.ledPos["anodeR"],False)
	def displayNum(self,num=8,lr="L"):
		which=self.numConst[num]
		if not ("N" in lr ):
			self.cleanPrev()
		for i in which:
			GPIO.output(self.ledPos[i],False)
		if "L" in lr:
			GPIO.output(self.ledPos["anodeL"],True)
		if "R" in lr:
			GPIO.output(self.ledPos["anodeR"],True)
	def displaySingleNum(self,num=99):
		self.cLock.acquire()
		try:
			self.Lnum=int(num / 10)
			self.Rnum=int(num % 10)
		finally:
			self.cLock.release()
		
		
	def setMap(self,mMap={"anodeL":11,"anodeR":12,"LA":16,"LB":18,"LC":21,"LD":22,"LE":15,"LF":19,"LG":13}):
		self.ledPos=mMap
	def restart(self):
		print("Number's display threading restarting....")
		self.disThreading=threading.Thread(target=self.displayThreading)
		self.disThreading.setDaemon(True)
		self.disThreading.start()
	def stopThreading(self):
		self.cLock.acquire()
		try:
			self.isStop=True
		finally:
			self.cLock.release()
	def displayThreading(self):
		print("Display threading start.")
		while(1):
			self.cLock.acquire()
			try:
				if self.isStop:
					self.cLock.release()
					self.cleanPrev()
					print("display")
					return
				self.cleanPrev()
				self.displayNum(num=self.Lnum,lr="L")
				time.sleep(0.005)
				self.cleanPrev()
				self.displayNum(num=self.Rnum,lr="R")
				time.sleep(0.005)
			finally:
				self.cLock.release()