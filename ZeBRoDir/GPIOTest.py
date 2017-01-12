import RPi.GPIO as GPIO

#set up GPIO using BCM numbering
#GPIO.setmode(GPIO.BCM)

#setup GPIO using board numbering
GPIO.setmode(GPIO.BOARD)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

