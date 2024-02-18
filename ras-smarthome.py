import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
import cv2
import time
from flask import Flask, request, abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

CGIR_SEND = 19
RED_LED = 16
BLUE_LED = 20
GREEN_LED = 21
SENSOR = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(CGIR_SEND, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

AC_ON_SHELL = "cgir send -c ./data/test_cgir.json -g19 AC_ON"
AC_OFF_SHELL = "cgir send -c ./data/test_cgir.json -g19 AC_OFF"
RED_SHELL = "cgir send -c ./data/test_cgir.json -g19 RED_LED"
BLUE_SHELL = "cgir send -c ./data/test_cgir.json -g19 BLUE_LED"
GREEN_SHELL = "cgir send -c ./data/test_cgir.json -g19 GREEN_LED"

app = Flask(__name__)
linebot_api = LineBotApi('')
handler = WebhookHandler('')

cam = cv2.VideoCapture(0)
now = datetime.now()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-line-signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as ivse:
        print(ivse)
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    text = ""
    try:
        if event.message.text == "電源つけて！":
            GPIO.cleanup()
            subprocess.call(AC_ON_SHELL, shell=True)
            text="電源を点けたよ！"
        elif event.message.text == "電源けして！":
            GPIO.cleanup()
            subprocess.call(AC_OFF_SHELL, shell=True)
            text="電源を消したよ！"
        elif event.message.text == "赤色にして！":
            GPIO.cleanup()
            subprocess.call(RED_SHELL, shell=True)
            text="LEDを「赤色」に変えたよ！"
        elif event.message.text == "青色にして！":
            GPIO.cleanup()
            subprocess.call(BLUE_SHELL, shell=True)
            text="LEDを「青色」に変えたよ！"
        elif event.message.text == "緑色にして！":
            GPIO.cleanup()
            subprocess.call(GREEN_SHELL, shell=True)
            text="LEDを「緑色」に変えたよ！"
        elif event.message.text:
            text="そのメッセージには対応できないよ！"
    except Exception as e:
        print(e)

    if event.message.text == "状況を教えて！":
        try:
            date = now.strftime("%Y%m%d_%H%M%S")
            path = "/home/pi/src/img/capture" + date + ".jpg"
            cv2.imwrite(path,cap)
            text = "今のお部屋の状況だよ！"
            linebot_api.reply_message(event.reply_token, ImageSendMessage(path))
        except Exception as e:
            print(e)
            

    print(text)
    linebot_api.reply_message(event.reply_token, TextSendMessage(text=text))


if __name__  == '__main__':
    app.run()

while True:
	ret,cap = cam.read()
	key = cv2.waitKey(1)
	cv2.imshow('frame', cap)
	try:
		if key == ord('q'):
			break
		elif (key == ord('s')):
			date = now.strftime("%Y%m%d_%H%M%S")
			path = "/home/pi/src/img/capture" + date + ".jpg"
			cam.release()
			w = cv2.imwrite(path,cap)
			linebot_api.reply_message(TextSendMessage(text="誰かが来たみたいだよ！"),ImageSendMessage(path))
			GPIO.output(BLUE_LED)
			print('Completed.')
	except Exception as e:
		print(e)
		print("Camera connection is" + ret)


GPIO.cleanup()
cv2.destroyAllWindows()