import logging
import RPi.GPIO as GPIO
_logger = logging.getLogger(__name__)


class RaspiShutter(object):
	def __init__(self, channel):

		self.ch = channel
		_logger.info("Starting RaspyShutter using the GPIO port %0d", self.ch)
		try:
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(self.ch, GPIO.OUT)
		except:
			_logger.info("Error setting GPIO port %0d", self.ch)
			self.ready=False
		GPIO.output(self.ch, False)
		self.state=GPIO.input(self.ch)
		self.ready=True		

	def get_state(self):
		_logger.info("Getting state GPIO port %0d", self.ch)
		state=GPIO.input(self.ch)
		return state

	def set_state(self, value):
		_logger.info("Setting state GPIO port %0d to %d", self.ch, value)
		GPIO.output(self.ch, value)		
		GPIO.input(self.ch)
		return True

	def close(self):
		GPIO.cleanup()
		
        
