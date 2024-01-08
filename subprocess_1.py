import RPi.GPIO as GPIO
import os
import subprocess
import time 

sensor = 26
irrp_sensor = 19
red_led = 16
blue_led = 20
green_led = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(irrp_sensor, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(blue_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)

red_shell = "cgir send -c ./src/data/test_cgir.json -g19 -w1 AC_ON RED_LED AC_OFF"
blue_shell = "cgir send -c ./src/data/test_cgir.json -g19 -w1 AC_ON BLUE_LED AC_OFF"
green_shell = "cgir send -c ./src/data/test_cgir.json -g19 -w1 AC_ON GREEN_LED AC_OFF"

counter = 0

while True:
    try:
        if(GPIO.input(sensor) == GPIO.HIGH | counter == 0):
            GPIO.output(red_led, 1)
            time.sleep(1)
            ret1 = subprocess.call(red_shell)
            time.sleep(3)
            counter = 1
        elif(GPIO.input(sensor) == GPIO.HIGH | counter == 1):
            GPIO.output(blue_led, 1)
            time.sleep(1)
            ret2 = subprocess.call(blue_shell)
            time.sleep(3)
            counter = 2
        elif(GPIO.input(sensor) == GPIO.HIGH | counter == 2):
            GPIO.output(green_led, 1)
            time.sleep(1)
            ret3 = subprocess.call(green_shell)
            time.sleep(3)
            counter = 0
        else:
            time.sleep(3)
            print("Not Found.")                 
    except KeyboardInterrupt:
        print("Program Stopped.")

GPIO.cleanup()