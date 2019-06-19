#!/bin/bash
#Install script for dependencies (works for raspberry pi3 ONLY)
#execute: sudo ./setup.sh

echo "Enabling SPI and I2C"
raspi-config nonint do_spi %d
raspi-config nonint do_i2c %d

echo "Installing packages for math"
apt-get update
apt-get install libatlas-base-dev liblapack-dev libblas-dev

echo "Install gpio control libraries"
apt-get install pigpio
systemctl enable pigpiod
systemctl start pigpiod

echo "Installing python libraries"
cd deps
pip3 install numpy-1.16.4-cp35-cp35m-linux_armv7l.whl
pip3 install pandas-0.24.1-cp35-cp35m-linux_armv7l.whl
pip3 install scikit_learn-0.20.2-cp35-cp35m-linux_armv7l.whl
pip3 install xgboost-0.81-cp35-cp35m-linux_armv7l.whl
pip3 install flask

echo "Setup successful"
echo "Run src/main.py to log the data in src/web/values.db"
echo "Run src/web/web.py to start the server"
