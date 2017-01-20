#!/usr/bin/env python

import time 
import picamera 
import time
import os
import glob
import RPi.GPIO as GPIO
import numpy as np

from smbus import SMBus

from datetime import datetime
from neopixel import *

bus = SMBus(1)
address = 0x04

LEDS		= 24	#amount of leds
PIN 		= 18	#GPIO / PIN 12
BRIGHTNESS 	= 55 	#min 0 / max 255

KLEUR_R		= 255
KLEUR_G		= 255
KLEUR_B		= 255

timeToSleep = 0.5

def writeNumber(value):
	l = list(value.split(',',4))
		
	print(type(int(l[1])))
	print(l)
	for i in range(0, len(l)):
		print(int(l[i]))
		bus.write_i2c_block_data(address,0,[int(l[i])])
	
	return -1

def readData():
	number = bus.read_byte(address)
	return number

def loopLed(ring, color):
	for i in range(ring.numPixels()):
		ring.setPixelColor(i,color)
		ring.show()
	
def resetLeds(ring, color, wait_ms=10):
	for i in range(ring.numPixels()):
		ring.setPixelColor(i, color)
		ring.show()

def callVision(file, extention):
        cmd = ('./vision1 '+file+extention+' 0')
	os.system(cmd)
	print "Einde programma"

def takePicture():
	textFile = open("previousPicture.txt","r")
	oldPictureFile = textFile.read()
	print "The old file whitch has been removed is: %s" % oldPictureFile
	textFile.close()

	os.remove(oldPictureFile.rstrip())

	loopLed(ring, Color(KLEUR_R, KLEUR_G, KLEUR_B))

	fileName = datetime.now().strftime("%Y%m%d-%H%M%S")

	time.sleep(timeToSleep)

	camera.rotation = 180

	camera.capture(fileName + '.jpg')

	newTextFile = open("previousPicture.txt", "w")
	newTextFile.write(fileName + '.jpg')
	newTextFile.close()

	resetLeds(ring,Color(0,0,0))

	fileExtention = '.jpg'

	print "The new file whitch is created is: %s%s" % (fileName, fileExtention)

	callVision(fileName, fileExtention)

def readVisionData():
        textFileVision = open("data.txt","r")
        dataFromVision = textFileVision.read()
        print "The data from the Vision system represents distance, rotation, Xvalue and Yvalue: %s" % dataFromVision
	writeNumber(dataFromVision)
	
def trigger():
	#GPIO.cleanup()
	if(GPIO.input(24) == 1):
		print ("trigger is high")
		return 1
	else:
		#print ("trigger is low")
		return 0
	return 1

if __name__ == '__main__':
	ring = Adafruit_NeoPixel(LEDS, PIN, 800000, 5, False, BRIGHTNESS)

	camera = picamera.PiCamera()

	camera.resolution=(800,600)

	ring.begin()
	resetLeds(ring,Color(0,0,0))

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

	triggerVar = 0

	print ("The program wil activate the raspberry pi with the vision systems and wil return the coordinates over I2C ZeBRo bus")

	while(1):
		triggerVar = trigger()
		if triggerVar == 1:
			takePicture()
			readVisionData()
		#var = input("Enter value: ")
		#if not var:
		#continue
		#writeNumber(var)
		#print("Sended value")
		#time.sleep(1)
		#number = readNumber()
		#print("Received digid", number)
