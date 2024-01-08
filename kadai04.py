import RPi.GPIO as GPIO
from time import sleep
import picamera

human_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(human_pin, GPIO.IN)

camera = picamera.PiCamera()

try:
    cnt = 0
    while True:
        human = GPIO.input(human_pin)
        if human == 0:
            print('OFF')
            sleep(1)
        else:
            cnt += 1
            print('ON ..... ', cnt)
            camera.capture('/home/pi/image{}.jpg'.format(cnt))
            sleep(1)
  
except KeyboardInterrupt:
    pass

GPIO.cleanup()
camera.close()