import cv2
import RPi.GPIO as GPIO
import time

sensor = 23
cnt = 0
path = f"./capture/image{cnt}.jpg"
cam = cv2.VideoCapture(0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN)

try:
    while True:
        ref,read = cam.read()
        if(GPIO.input(sensor) == GPIO.HIGH):
            cnt += 1
            cv2.imwrite(path,read)
            print(f"Detected. Count{cnt}")
            time.sleep(1)
        elif(GPIO.input(sensor) == GPIO.LOW):
            print('OFF')
            time.sleep(1)
        else:
            break
        
except KeyboardInterrupt:
    pass

cam.release()
GPIO.cleanup()
