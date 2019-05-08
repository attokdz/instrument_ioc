import logging
import serial
_logger = logging.getLogger(__name__)


class AttoValve(object):
	def __init__(self, port, baudrate=115200):
		
		self.port = port
		_logger.info("Starting AttoTechValse at port: %s", self.port)
		try:
			self.fh=serial.Serial(self.port)
			self.fh.baudrate=baudrate
			self.isrunning=False
			self.fh.flushOutput()
			self.fh.readline()
			self.fh.readline()
			self.ready=True
		except:
			_logger.info("Error setting port %s", self.port)
			self.ready=False

	def getVoltage(self):
		self.fh.flushOutput()
		self.fh.write("GetHV\n")
		val=self.fh.readline().split(" ")[1]
		try:
			fval=float(val)
			return fval
		except:
			return -1

	def setVoltage(self, value):
		self.fh.flush()
		self.fh.write("SetHV %d\n"%value)
		self.fh.flush()
		print(self.fh.readline())

	def getDuration(self):
		self.fh.flushOutput()
		self.fh.write("GetDuration\n")
		val=self.fh.readline().split(":")[1].split("\r")[0]
		try:
			fval=float(val)
			return fval
		except:
			return -1

	def setDuration(self, value):
		self.fh.flush()
		self.fh.write("SetDuration %d\n"%value)
		print(self.fh.readline())

	def getDelay(self):
		self.fh.flushOutput()
		self.fh.write("GetDelay\n")
		val=self.fh.readline().split(":")[1].split("\r")[0]
		try:
			fval=float(val)
			return fval
		except:
			return -1

	def setDelay(self, value):
		self.fh.flush()
		self.fh.write("SetDelay %d\n"%value)
		_logger.info(self.fh.readline())

	def setRun(self, value):
		self.fh.flush()
		if value:
			self.fh.write("Start\n")
			self.isrunning=True
		elif not(value):
			self.fh.write("Stop\n")
			self.isrunning=False
		_logger.info(self.fh.readline())

	def getRun(self):
		return self.isrunning
		

	def close(self):
		self.fh.close()
		
        
