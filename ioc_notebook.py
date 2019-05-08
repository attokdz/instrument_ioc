from pcaspy import  Driver
from threading import Thread 
import time



pvdb =  {
    'GenerationMedium' : {
        'type': 'string',
		'unit': '-'
    },
	
	'MCPVOLTAGE' : {
        'type': 'int',
	'unit': 'Volts'
    },
	
	'SCREENVOLTAGE' : {
        'type' : 'int',
	'unit' : 'Volts'
    },
	
	'SAMPLE' : {
        'type' : 'string'
    },
	
	'FIBERINPUT' : {
        'type' : 'float',
	'unit' : 'Watts'
    },
	
	'FIBEROUTPUT' : {
        'type': 'float',
	'unit': 'Watts'
    },

	'FIBERPRESSURE' : {
        'type': 'float',
	'unit': 'bars'
    },

	'FIBERMEDIA' : {
        'type': 'float',
	'unit': 'bars'
    },
	
	'FFILTER' : {
        'type': 'string'
    },
	
	'SPECFILTER' : {
        'type' : 'string'
    },

	'Status' : {
	'type' : 'int',
	'value': 0,
    },
	 	
 }

def make_pvs(prefix):
	pvs={}
	for i in pvdb:
		pvs.update({"%s:%s"%(prefix, i): pvdb[i]})
	return pvs
 

 
class NoteBookIoc:
	def __init__(self, parent, prefix):
		self.parent=parent
		self.prefix=prefix
		self.setParam('Status', True)


		
	def read(self, reason):	
		return self.getParam(reason)
			
	def write(self, reason, value):
		self.setParam(reason, value)
		self.updatePVs()

	def setParam(self, reason, value):
		return self.parent.setParam("%s:%s"%(self.prefix, reason), value)

	def getParam(self, reason):
		return self.parent.getParam("%s:%s"%(self.prefix, reason))

	def updatePVs(self):
		return self.parent.updatePVs()  
	
		
