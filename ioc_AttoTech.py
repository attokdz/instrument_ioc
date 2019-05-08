from threading import Thread
from time import sleep
import logging

_logger = logging.getLogger("AttoValve")

pvdb = {
    "Voltage": {
        'type': "float",
        'hihi': 300,
        'high': 200,
        'low': 50,
        'lolo': 0,
		'HOPR': 300,
		'LOPR': 0,
        'prec': 3
    },

    "Duration": {
        "type": "float"
    },

    "Delay": {
        "type": "float"
    },

    "Run": {
        "type": "int"
    },

    "Status": {
        "type": "int"
    }
}


def make_pvs(prefix):
	pvs={}
	for i in pvdb:
		pvs.update({"%s:%s"%(prefix, i): pvdb[i]})
	return pvs
 

class EpicsAttoTechDriver():

    def __init__(self, driver, parent, prefix):
        _logger.info("Starting epics driver for AttoValve.")
        self.valve_driver = driver
        self.parent=parent
        self.prefix=prefix
        self.setParam("Status", True)
        self.updatePVs()

    def read(self, reason):
        if reason=="Voltage":
           return self.getVoltage()
        elif reason=="Duration":
           return self.getDuration()
        elif reason=="Delay":
           return self.getDelay()
        elif reason=="Status":
           return self.getStatus()
        elif reason=="Run":
           return self.getRun()

 
    
    def write(self, reason, value):
        if reason=="Voltage":
           self.setVoltage(value)
        elif reason=="Duration":
           self.setDuration(value)
        elif reason=="Delay":
           self.setDelay(value)
        elif reason=="Run":
           self.setRun(value)

    def setParam(self, reason, value):
        return self.parent.setParam("%s:%s"%(self.prefix, reason), value)

    def	getParam(self, reason):
        return self.parent.getParam("%s:%s"%(self.prefix, reason))

    def updatePVs(self):
        return self.parent.updatePVs()

    def setVoltage(self, value):
            try:
                _logger.debug("Setting Voltage to  '%f'. ", value)
                self.valve_driver.setVoltage(value)
                rb=self.valve_driver.getVoltage()
                if rb>=0:
                	self.setParam("Voltage", rb)
                	self.updatePVs()
            except:
                _logger.exception("Could not set Voltage to '%f' .", value)
                self.setParam("Status", False)
                self.updatePVs()


    def setDelay(self, value):
            try:
                _logger.debug("Setting Delay to  '%f'. ", value)
                self.valve_driver.setDelay(value)
                rb=self.valve_driver.getDelay()
                if rb>0:
                	self.setParam("Delay", rb)
                	self.updatePVs()
            except:
                _logger.exception("Could not set Delay to '%f' .", value)
                self.setParam("Status", False)
                self.updatePVs()


    def setDuration(self, value):
            try:
                _logger.debug("Setting opening to  '%f'. ", value)
                self.valve_driver.setDuration(value)
                rb=self.valve_driver.getDuration()
                if rb>0:
                	self.setParam("Duration", rb)
                	self.updatePVs()
            except:
                _logger.exception("Could not set opening to '%f' .", value)
                self.setParam("Status", False)
                self.updatePVs()

    def setRun(self, value):
            try:
                _logger.debug("Setting state to  '%d'. ", value)
                self.valve_driver.setRun(value)
                rb=self.valve_driver.getRun()
                if rb>=0:
                    self.setParam("Run", rb)
                    self.updatePVs()
            except:
                _logger.exception("Could not set state to '%d' .", value)
                self.setParam("Status", False)
                self.updatePVs()



    def getDuration(self):
            try:
                _logger.debug("Getting opening time")
                rb=self.valve_driver.getDuration()
                if rb>0:
                    self.setParam("Duration", rb)
                    self.updatePVs()
                    return rb
            except:
                _logger.exception("Could not get opening time")
                self.setParam("Status", False)
                self.updatePVs()

    def getDelay(self):
            try:
                _logger.debug("Getting Delay")
                rb=self.valve_driver.getDelay()
                if rb>0:
                    self.setParam("Delay", rb)
                    self.updatePVs()
                    return rb
            except:
                _logger.exception("Could not get Delay.")
                self.setParam("Status", False)
                self.updatePVs()

    def getVoltage(self):
            try:
                _logger.debug("Getting Voltage")
                rb=self.valve_driver.getVoltage()
                if rb>=0:
                    self.setParam("Voltage", rb)
                    self.updatePVs()
                    return rb
            except:
                _logger.exception("Could not get Voltage")
                self.setParam("Status", False)
                self.updatePVs()

    def getRun(self):
            try:
                _logger.debug("Getting state")
                rb=self.valve_driver.getRun()
                if rb>=0:
                    self.setParam("Run", rb)
                    self.updatePVs()
                    return rb
            except:
                _logger.exception("Could not get state")
                self.setParam("Status", False)
                self.updatePVs()

    def getStatus(self):
      return self.getParam("Status")

            
           
