import Adafruit_MCP4725
from Adafruit_BME280 import *
from time import sleep
import spidev
from statistics import mean
import sqlite3 as sql
import pigpio

pi = pigpio.pi()

gain = 3.2
hval = 0
sval = 0
mux = 0

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 100000
spi.mode = 0b00

hv = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)
sv = Adafruit_MCP4725.MCP4725(address=0x61, busnum=1)
bme = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

def set_sv(volt):
	global sv
	global sval
	val = int((float(volt)/gain)*4096/3.3)
	if val > sval:
		i = sval
		while i<val:
			sv.set_voltage(i, False)
			i = i + 1
			sleep(0.001)
		sv.set_voltage(val, False)
	elif val < sval:
		i = sval
		while i>val:
			sv.set_voltage(i, False)
			i = i - 1
			sleep(0.001)
		sv.set_voltage(val, False)
	sval = val
	print("sv set to ", volt)

def set_hv(volt):
	global hv
	global hval
	val = int((float(volt)/gain)*4096/3.3)
	if val > hval:
		i = hval
		while i<val:
			hv.set_voltage(i, False)
			i = i + 1
			sleep(0.001)
		hv.set_voltage(val, False)
	elif val < hval:
		i = hval
		while i>val:
			hv.set_voltage(i, False)
			i = i - 1
			sleep(0.001)
		hv.set_voltage(val, False)
	hval = val
	print("hv set to ", volt)

def read_adc():
	global mux
	adc_data = [0]*200
	for i in range(0,200):
		adc_raw = spi.readbytes(3)
		adc_data[i] = -1
		while adc_raw[0]==255:
			adc_raw = spi.readbytes(3)
		adc_data[i] = (adc_raw[0]*0x10000 + adc_raw[1]*0x100 + adc_raw[2])*3.3/(0x100000)
		#print(adc_raw)
	raw_adc = round(mean(adc_data),4)
	sensor_val = (3.3-raw_adc)/(10**(1+mux)) #convert to mA 
	return [raw_adc, sensor_val]

def read_bme():
	global bme
	degrees = round(bme.read_temperature(),2)
	#pascals = bme.read_pressure()
	humidity = round(bme.read_humidity(),2)
	return [degrees, humidity]

def log_db(co2, temp, hum):
	with sql.connect("web/values.db") as con:
		cur = con.cursor()
		cur.execute('''CREATE TABLE IF NOT EXISTS sensor (id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, co2 REAL, temp REAL, hum REAL)''')
		cur.execute("INSERT INTO sensor (co2, temp, hum) VALUES (?,?,?)", (co2,temp,hum))
		con.commit()

def set_mux(config):
	if config==0:
		pi.write(5,0)
		pi.write(6,0)
	elif config==1:
		pi.write(5,1)
		pi.write(6,0)
	elif config==2:
		pi.write(5,0)
		pi.write(6,1)
	elif config==3:
		pi.write(5,1)
		pi.write(6,1)

set_mux(mux)
set_sv(4.3)
set_hv(0)

try:
	while True:
		[raw_adc, sensor_cur] = read_adc()
		[temp, hum] = read_bme()
		if(raw_adc>3.1 and mux>0):
			mux = mux-1
			set_mux(mux)
		elif(raw_adc<1 and mux<3):
			mux = mux+1
			set_mux(mux)
		print(raw_adc, sensor_cur, mux, temp, hum)
		log_db(sensor_cur, temp, hum)

except KeyboardInterrupt:
	print("exit")
	spi.close()

