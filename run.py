import sys
import logging
import ioc_notebook
import ioc_RaspiGPIO 
import ioc_AttoTech
import ioc_merge as ioc

from argparse import ArgumentParser
from pcaspy import SimpleServer
from pcaspy.tools import ServerThread
from PyRaShutter import RaspiShutter
from AttoTech import AttoValve


def main():
	parser = ArgumentParser()
	parser.add_argument("--ioc_prefix", type=str, help="Global prefix of the IOC.")

	parser.add_argument("--pump_prefix", type=str, help="Prefix for pump shutter.")
	parser.add_argument("--pump_port", type=int, help="GPIO port of pump.")

	parser.add_argument("--probe_prefix", type=str, help="Prefix for probe shutter.")
	parser.add_argument("--probe_port", type=int, help="GPIO port of probe.")

	parser.add_argument("--valve_prefix", type=str, help="Prefix for pulse valve.")
	parser.add_argument("--valve_port", type=str, help="Serial port of pulse valve.")

	parser.add_argument("--notebook_prefix", type=str, help="Prefix for Notebook.")
	parser.add_argument("--log_level", type=str, help="Logging level for the iocs")

	arguments = parser.parse_args()


	logging.basicConfig(stream=sys.stdout, level=arguments.log_level)
	_logger = logging.getLogger(arguments.ioc_prefix[:-1])

	

	pvdb={}
	pvdb.update(ioc_notebook.make_pvs(arguments.notebook_prefix))
	pvdb.update(ioc_RaspiGPIO.make_pvs(arguments.pump_prefix))
	pvdb.update(ioc_RaspiGPIO.make_pvs(arguments.probe_prefix))
	pvdb.update(ioc_AttoTech.make_pvs(arguments.valve_prefix))

	_logger.info("Starting ioc with prefix '%s'.",	arguments.ioc_prefix)
	server = SimpleServer()
	server.createPV(prefix=arguments.ioc_prefix, pvdb=pvdb)


	#Setting devices drivers
	PumpShutter_driver=RaspiShutter(arguments.pump_port)
	if not(PumpShutter_driver.ready):
		_logger.ERROR("Error connecting to Pump shutter")
	HHGShutter_driver=RaspiShutter(arguments.probe_port)
	if not(HHGShutter_driver.ready):
		_logger.ERROR("Error connecting to ProbeShutter")
	valve_driver=AttoValve(arguments.valve_port)
	if not(valve_driver.ready):
		_logger.ERROR("Error connecting to AttoValve")

	driver = ioc.ioc_raspi1()

	valve_ioc=ioc_AttoTech.EpicsAttoTechDriver(valve_driver, driver, arguments.valve_prefix)
	pumpshutter_ioc=ioc_RaspiGPIO.EpicsRaspiShutterDriver(PumpShutter_driver, driver, arguments.pump_prefix)
	hhgshutter_ioc=ioc_RaspiGPIO.EpicsRaspiShutterDriver(HHGShutter_driver, driver, arguments.probe_prefix)
	notebook_ioc=ioc_notebook.NoteBookIoc(driver, arguments.notebook_prefix)

	driver.add_ioc(valve_ioc)
	driver.add_ioc(pumpshutter_ioc)
	driver.add_ioc(hhgshutter_ioc)
	driver.add_ioc(notebook_ioc)

	server_thread = ServerThread(server)	
	server_thread.start()	
	while not(raw_input("Press 'q' to quit: ")=="q"):
		pass
	server_thread.stop()	
	_logger.info("User requested ioc termination. Exiting.")
	PumpShutter_driver.close()
	HHGShutter_driver.close()
	valve_driver.close()

if __name__ == "__main__":
    main()
