import serial
from time import sleep

node1 = serial.Serial(port='/dev/rfcomm0', baudrate=9600)
node2 = serial.Serial(port='/dev/rfcomm1', baudrate=9600)

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
	node.write([64])
	data_str = node.read(11)
	print(data_str)
	
def set_sv_nodes(no, val):
	if(no==1):
		node = node1
	elif(no==2):
		node = node2
	else:
		return
	node.write([64])
	data_str = node.read(11)
	print(data_str)

def read_data(no):
	if(no==1):
		node = node1
	elif(no==2):
		node = node2
	else:
		return
	node.write([64])
	data_str = node.read(11)
	print(data_str)
