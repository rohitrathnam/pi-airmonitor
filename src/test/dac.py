import Adafruit_MCP4725
from time import sleep

gain = 3.2
hval = 0
sval = 0

hv = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)
sv = Adafruit_MCP4725.MCP4725(address=0x61, busnum=1)

def sv_set(volt):
	global sv
	global sval
	val = int((float(volt)/gain)*4096/3.3)
	if val > sval:
		for i in range(sval, val):
			sv.set_voltage(i, False)
			sleep(0.01)
		sv.set_voltage(val, False)
	elif val < sval:
		for i in range(sval, val, -1):
			sv.set_voltage(i, False)
			sleep(0.01)
		sv.set_voltage(val, False)
	sval = val

def hv_set(volt):
	global hv
	global hval
	val = int((float(volt)/gain)*4096/3.3)
	if val > hval:
		for i in range(hval, val):
			hv.set_voltage(i, False)
			sleep(0.01)
		hv.set_voltage(val, False)
	elif val < hval:
		for i in range(hval, val, -1):
			hv.set_voltage(i, False)
			sleep(0.01)
		hv.set_voltage(val, False)
	hval = val
