#!/usr/bin/env python

import time 
import picamera 
import time
import os
import glob

from datetime import datetime
from neopixel import *

LEDS		= 24	#amount of leds
PIN 		= 18	#GPIO / PIN 12
BRIGHTNESS 	= 55 	#min 0 / max 255

KLEUR_R		= 255
KLEUR_G		= 255
KLEUR_B		= 255

timeToSleep 	= 0.5

def loopLed(ring, color):
	for i in range(ring.numPixels()):
		ring.setPixelColor(i,color)
		ring.show()
	
def resetLeds(ring, color, wait_ms=10):
	for i in range(ring.numPixels()):
		ring.setPixelColor(i, color)
		ring.show()

if __name__ == '__main__':
	ring = Adafruit_NeoPixel(LEDS, PIN, 800000, 5, False, BRIGHTNESS)

	camera = picamera.PiCamera()	
	
	ring.begin()
	resetLeds(ring,Color(0,0,0))
	
	textFile = open("previousPicture.txt", "r")
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
