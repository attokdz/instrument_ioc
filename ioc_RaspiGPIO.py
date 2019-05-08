from threading import Thread
from time import sleep
import logging

_logger = logging.getLogger("RaspiShutter")

pvdb = {
    "State": {
        "type": "int"
    },

    # This is a special case - do not include it in write_pvname_to_shimatzu_property.
    "Status": {
        "type": "int"
    }
}

def make_pvs(prefix):
	pvs={}
	for i in pvdb:
		pvs.update({"%s:%s"%(prefix, i): pvdb[i]})
	return pvs



class EpicsRaspiShutterDriver:

    def __init__(self, driver, parent, prefix):
        self.parent=parent
        self.prefix=prefix
        self.shutter_driver = driver
	_logger.info("Starting epics driver for raspi GPIO at port %02d."%self.shutter_driver.ch)
	self.setParam("Status", True)

    def read(self, reason):
        if reason=="State":
           return self.getState()
    
    def write(self, reason, value):
        if reason=="State":
           self.setState(value)

    def setParam(self, reason, value):
        return self.parent.setParam("%s:%s"%(self.prefix, reason), value)

    def	getParam(self, reason):
        return self.parent.getParam("%s:%s"%(self.prefix, reason))

    def updatePVs(self):
        return self.parent.updatePVs()        

    def setState(self, value):
            try:
                _logger.debug("Setting shutter to  '%d'. ", value)
                self.shutter_driver.set_state(value)
                self.setParam("State", value)
                self.updatePVs()
            except:
               _logger.exception("Could not set shutter state to '%d' .", value)
               self.setParam("Status", False)
               self.updatePVs()

    def getState(self):
            try:
                _logger.debug("getting shutter to state'. ")
                value=self.shutter_driver.get_state()
                return value
            except:
               _logger.exception("Could not read shutter state to '%d' .")
               self.setParam("Status", False)
               self.updatePVs()
               return -1

            
           
