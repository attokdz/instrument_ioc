from pcaspy import  Driver
from threading import Thread 
import logging
import numpy as np
import time
_logger = logging.getLogger("Raspi1")





 
class ioc_raspi1(Driver):
	def __init__(self):
		"""Get array of pair [cam, Prefixs] where prefix is xxxx:PREFIX:yyyy""" 
		Driver.__init__(self)
		self.ioc=[]
		self.prefix=[]		


	def add_ioc(self, ioc):
		self.ioc.append(ioc)
		self.prefix.append(self.ioc[-1].prefix)
		_logger.info("Added ioc with prefix: %s."%self.prefix[-1])

	def read(self, reason):
		pre=reason.split(":")
		print(reason)
		if pre[0] in self.prefix:
			inx=self.prefix.index(pre[0])
		else:
			return
		
		answ=self.ioc[inx].read(pre[1])
		self.updatePVs()

		return self.getParam(reason)
			
	def write(self, reason, value):
		pre=reason.split(":")
		if pre[0] in self.prefix:
			inx=self.prefix.index(pre[0])
		
		answ=self.ioc[inx].write(pre[1], value)
		self.updatePVs()

		
		
	
		
