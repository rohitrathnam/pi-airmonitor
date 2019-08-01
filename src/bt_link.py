import serial
from time import sleep

READ = 64
SET_SV = 63
SET_HV = 62

node1 = serial.Serial(port='/dev/rfcomm0', baudrate=9600)
node2 = serial.Serial(port='/dev/rfcomm1', baudrate=9600)

def init_bt():
	node1.close()
	node2.close()
	
	node1.open()
	node2.open()

def read_data(no):
	if(no==1):
		node = node1
	elif(no==2):
		node = node2
	else:
		return
	node.write([READ])
	data_str = node.read(11)
	print(data_str)
	
def set_sv_nodes(no, val):
	if(no==1):
		node = node1
	elif(no==2):
		node = node2
	else:
		return
	node.write([SET_SV,val])
	print("set sv to ",val)
	
def set_hv_nodes(no, val):
	if(no==1):
		node = node1
	elif(no==2):
		node = node2
	else:
		return
	node.write([SET_HV,val])
	print("set hv to ",val)

init_bt()
