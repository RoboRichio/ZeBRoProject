#!/usr/bin/env python

from smbus import SMBus
import time

#for raspberrypi version 1, use "bus=smbus.SMBus(0)"
bus = SMBus(1) #1 indicates /dev/i2c-1 
#This is the address we setup in the arduino program
address = 0x04

def writeNumber(value):
	bus.write_byte(address, int(value))
	#bus.write_byte_data(address, 0, value)
	return -1

def readNumber():
	number = bus.read_byte(address)
	#number = bus.read_byte_data(address, 1)
	return number
	
while True:
	var = input("Enter 1-9: ")
	if not var:
		continue

	writeNumber(var)

	print("Raspberry Pi: Hi Arduino, I send you ", var)

	#sleep one second

	time.sleep(1)

	number = readNumber()
	print("Arduino: Hey Raspberry Pi, i received a digid", number)
