#!/usr/bin/python3

import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

while 1:
        # read from Arduino
        input = ser.read()
        print ("Read input " + input.decode("utf-8") + " from Arduino")