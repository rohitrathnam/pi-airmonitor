# pi-airmonitor

Enable SPI, I2C and UART in raspi-config

To use with screen, check commented spi config in main.py. Also add "dtoverlay=spi1-1cs,cs0_pin=26" to /boot/config.txt to enable SPI1, connect ADC pins to SPI1 pins of pi

Bluetooth code won't work with pi 2

For RTC, edit /boot/config.txt and add the following to last line:
dtoverlay=i2c-rtc,ds3231

Update your system time using ntpdate
To update system time into RTC use hwclock -w

For more details on time check https://www.raspberrypi.org/forums/viewtopic.php?t=161133
