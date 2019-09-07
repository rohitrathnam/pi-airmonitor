#!/bin/bash
#Install script for dependencies (works for raspberry pi3 ONLY)
#execute: sudo ./setup.sh

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
pip3 install flask
pip3 install Adafruit_PureIO

echo "Setup successful"
echo "Run src/main.py to log the data in src/web/values.db"
echo "Run src/web/web.py to start the server"
echo "Follow https://www.raspberrypi.org/forums/viewtopic.php?p=1007463#p1007463"
