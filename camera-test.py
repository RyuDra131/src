import cv2
import requests
import RPi.GPIO as GPIO
import time
# import multiprocessing as mp
from datetime import datetime 

LED = 18
SENSOR = 23

tekito=""
test=""

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)

cam = cv2.VideoCapture(0)
now = datetime.now()

def send_message(Discovery_time):
    url = "https://notify-api.line.me/api/notify" 
    headers = {"Authorization" : "Bearer "+ tekito}
    files = {'imageFile': open(path, "rb")}
    message =  (now.strftime("%Y%mm%dd_%Hh%Mm%Ss"),"Fliming has been completed.")
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload, files=files)

# def check():
# 	while True:
# 		if(GPIO.input(SENSOR) == GPIO.HIGH):
# 			print('1')
# 			time.sleep(0.5)
# 		elif(GPIO.input(SENSOR) == GPIO.LOW):
# 			print('0')
# 			time.sleep(0.5)
# 		else:
# 			break

while True:
	ret,cap = cam.read()
	key = cv2.waitKey(1)
	cv2.imshow('frame', cap)
	try:
		if key == ord('q'):
			break
		elif (key == ord('s')) | (GPIO.input(SENSOR) == GPIO.HIGH):
			date = now.strftime("%Y%m%d_%H%M%S")
			path = "/home/pi/Desktop/capture" + date + ".jpg"
			cam.release()
			w = cv2.imwrite(path,cap)
			send_message(path)
			GPIO.output(LED)
			print('Completed.')
	except Exception as e:
		print(e)
		print("Camera connection is" + ret)


GPIO.cleanup()
cv2.destroyAllWindows()
