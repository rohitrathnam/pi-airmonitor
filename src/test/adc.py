import spidev
from time import sleep
#import wiringpi
'''
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(5,1)
wiringpi.pinMode(6,1)
wiringpi.digitalWrite(5,0)
wiringpi.digitalWrite(6,0)
'''
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.mode = 0b00
val = 0

try:
	while True:
		#wiringpi.digitalWrite(25,0)
		#sleep(0.020)
		val = spi.readbytes(3)
		#wiringpi.digitalWrite(25,1)
		if 1: #val[0]!=255:
			data = (val[0]*0x10000 + val[1]*0x100 + val[2])*3.24/(0x200000)
			print(data)
			print(val)
			sleep(0.5)
except KeyboardInterrupt:
	spi.close()
