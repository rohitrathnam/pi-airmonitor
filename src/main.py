import MCP4725
from Adafruit_BME280 import *
from time import sleep
import spidev
from statistics import mean
import sqlite3 as sql
import pigpio
import adxl345
import honeywell_hpma115s0 as pmsensor
import ads1115
import serial
from influxdb import InfluxDBClient

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import threading

MUX0 = 5
MUX1 = 6

pi = pigpio.pi()

gain = 3.2
hval = 0
sval = 0
mux = 0
new_sv = 0
new_hv = 0
global settings_flag
settings_flag = 0

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 100000
spi.mode = 0b00

hv = MCP4725.MCP4725(address=0x60)
sv = MCP4725.MCP4725(address=0x61)
bme = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
pm = pmsensor.Honeywell()
adxl = adxl345.ADXL345()
ads = ads1115.ADS1115()

node1 = serial.Serial(port='/dev/rfcomm0', baudrate=9600, timeout=8)
node2 = serial.Serial(port='/dev/rfcomm1', baudrate=9600, timeout=8)

db = InfluxDBClient(database='log')

def set_sv(volt):
	global sv
	global sval
	val = int((float(volt)/gain)*4096/3.3)
	if val > sval:
		i = sval
		while i<val:
			sv.set_voltage(i, False)
			i = i + 1
			sleep(0.002)
		sv.set_voltage(val, False)
	elif val < sval:
		i = sval
		while i>val:
			sv.set_voltage(i, False)
			i = i - 1
			sleep(0.002)
		sv.set_voltage(val, False)
	sval = val
	set_sv_node(node1, volt)
	set_sv_node(node2, volt)
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
			sleep(0.002)
		hv.set_voltage(val, False)
	elif val < hval:
		i = hval
		while i>val:
			hv.set_voltage(i, False)
			i = i - 1
			sleep(0.002)
		hv.set_voltage(val, False)
	hval = val
	set_hv_node(node1, volt)
	set_hv_node(node2, volt)
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

def log_db(gas, gas_raw, mux, temp, hum, pm25, pm10, acc_x, acc_y, acc_z, ldr, n1_gas, n1_temp, n1_hum, n2_gas, n2_temp, n2_hum):
	with sql.connect("log.db") as con:
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, gas REAL, gas_raw REAL, mux INTEGER, temp REAL, hum REAL, pm25 INTEGER, pm10 INTEGER, acc_x REAL, acc_y REAL, acc_z REAL, ldr INTEGER, n1_gas REAL, n1_temp REAL, n1_hum REAL, n2_gas REAL, n2_temp REAL, n2_hum REAL)")
		cur.execute("INSERT INTO log (gas, gas_raw, mux, temp, hum, pm25, pm10, acc_x, acc_y, acc_z, ldr, n1_gas, n1_temp, n1_hum, n2_gas, n2_temp, n2_hum) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (gas, gas_raw, mux, temp, hum, pm25, pm10, acc_x, acc_y, acc_z, ldr, n1_gas, n1_temp, n1_hum, n2_gas, n2_temp, n2_hum))
		con.commit()

def log_idb(gas, gas_raw, mux, temp, hum, pm25, pm10, acc_x, acc_y, acc_z, ldr, n1_gas, n1_temp, n1_hum, n2_gas, n2_temp, n2_hum):
	json = [
		{
		"measurement":"airmonitor",
		"fields":{
		"gas":gas,
		"gas_raw":gas_raw, 
		"mux":mux, 
		"temp":temp, 
		"hum":hum, 
		"pm25":pm25, 
		"pm10":pm10, 
		"acc_x":acc_x, 
		"acc_y":acc_y, 
		"acc_z":acc_z, 
		"ldr":ldr, 
		"n1_gas":n1_gas, 
		"n1_temp":n1_temp, 
		"n1_hum":n1_hum, 
		"n2_gas":n2_gas, 
		"n2_temp":n2_temp, 
		"n2_hum":n2_hum
		}}]
	db.write_points(json)

def set_mux(config):
	if config==0:
		pi.write(MUX0,0)
		pi.write(MUX1,0)
	elif config==1:
		pi.write(MUX0,1)
		pi.write(MUX1,0)
	elif config==2:
		pi.write(MUX0,0)
		pi.write(MUX1,1)
	elif config==3:
		pi.write(MUX0,1)
		pi.write(MUX1,1)

def read_node(node):
	#if node.isOpen():
	#	node.close()
	#node.open()
	node.write(b'@')
	strin = node.readline()[0:-2].decode('utf-8')
	#node.close()
	return strin.split(' ')

def set_hv_node(node, hv):
	#if node.isOpen():
	#	node.close()
	#node.open()
	#sleep(0.1)
	node.write(b'>'+bytes([int(hv*10)]))
	name = node.readline()
	#node.close()
	print('node '+str(name)+str(hv))

def set_sv_node(node, sv):
	#if node.isOpen():
	#	node.close()
	#node.open()
	#sleep(0.1)
	node.write(b'?'+bytes([int(sv*10)]))
	name = node.readline()
	#node.close()
	print('node '+str(name)+str(sv))

'''
@app.route('/')
def home():
	con = sql.connect("log.db")

	with con:
		cur = con.execute("SELECT * FROM log ORDER BY id DESC LIMIT 1")
		for row in cur:
			print("served ", row)
	return render_template('home.html', rows=row)
'''

@app.route('/status')
def status():
	return render_template("status.html",rows = [sval*gain*3.3/4096, hval*gain*3.3/4096])

@app.route('/settings')
def settings():
	return render_template("form.html")

@app.route('/change',methods = ['POST', 'GET'])
def change():
	global new_sv
	global new_hv
	if request.method == 'POST':
		new_sv = float(request.form['sv'])
		new_hv = float(request.form['hv'])
		global settings_flag
		settings_flag = 1
		sleep(1)
	return redirect(url_for('status'))

def webserver():
	print("Flask init success")
	app.run(host='0.0.0.0', port=80, debug=False)


if __name__ == '__main__':
	#webserver()
	
	if node1.isOpen():
		node1.close()
	if node2.isOpen():
		node2.close()
	web = threading.Thread(target=webserver)
	web.daemon = True
	web.start()
	node1.open()
	node2.open()
	set_mux(mux)
	set_sv(4.3)
	set_hv(5.9)

	try:
		while True:
			if settings_flag==1:
				set_sv(round(new_sv,1))
				set_hv(round(new_hv,1))
				settings_flag = 0
			[raw_adc, sensor_cur] = read_adc()
			[temp, hum] = read_bme()
			if(raw_adc>3.1 and mux>0):
				mux = mux-1
				set_mux(mux)
			elif(raw_adc<1 and mux<3):
				mux = mux+1
				set_mux(mux)
			print("sensor ", raw_adc, sensor_cur, mux)
			print("bme ", temp, hum)
			pm_data = pm.read()
			print("pm sensor ", pm_data.pm10, pm_data.pm25)
			acc = adxl.getAxes(True)
			print("acc ", acc['x'], acc['y'], acc['z'])
			ldr = ads.readADCSingleEnded()
			ldr = int(ldr)
			print("ldr ", ldr)
			n1 = read_node(node1)
			print("node1 ", n1)
			n2 = read_node(node2)
			print("node2 ", n2)
			log_idb(sensor_cur, raw_adc, mux, temp, hum, pm_data.pm25, pm_data.pm10, acc['x'], acc['y'], acc['z'], ldr, n1[0], n1[1], n1[2], n2[0], n2[1], n2[2])
			#use log_db function for sqlite debug db

	except KeyboardInterrupt:
		print("exit")
		spi.close()
		node1.close()
		node2.close()
