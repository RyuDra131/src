import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
import cv2
import time
import requests
from picamera import PiCamera
from datetime import datetime
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
linebot_api = LineBotApi('BOT_ACCESS_TOKEN')
handler = WebhookHandler('CHANNEL_SECRET')
TOKEN = 'CHANNEL_TOKEN'

path = "/home/pi/src/img/capture/image.jpg"

now = datetime.now()

def smarthome_for_send_message(sma):
    url = "https://notify-api.line.me/api/notify" 
    headers = {"Authorization" : "Bearer "+ TOKEN}
    files = {'imageFile': open(path, "rb")}
    message =  (now.strftime("%Y/%m/%d_%H:%M:%S"),"(らずすまより)今のお部屋の状況だよ！")
    payload = {"message" :  message} 
    req = requests.post(url, headers = headers, params=payload, files=files)

def image_send_message():
    try:
        cam = PiCamera()
        cam.capture(path)
        cam.close()
        frontal_face = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bodys = frontal_face.detectMultiScale(gray)
        for(x, y, w, h) in bodys:
            imgs = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
        save_img = cv2.imwrite(path,imgs)
        smarthome_for_send_message(save_img)
    except Exception:
        smarthome_for_send_message(img)


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
    path = "/home/pi/src/img/capture/image.jpg"
    try:
        if event.message.text == "電源つけて！":
            GPIO.cleanup()
            subprocess.call(AC_ON_SHELL, shell=True)
            text="電源を点けたよ！"
        elif event.message.text == "電源きって！":
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
        elif event.message.text == "エアコンつけて！":
            GPIO.cleanup()
            subprocess.call(GREEN_SHELL, shell=True)
            text="エアコンをつけたよ！" 
        elif event.message.text == "エアコンけして！":
            GPIO.cleanup()
            subprocess.call(GREEN_SHELL, shell=True)
            text="エアコンを消したよ！" 
        elif event.message.text == "部屋の電気つけて！":
            GPIO.cleanup()
            subprocess.call(GREEN_SHELL, shell=True)
            text="部屋の電気をつけたよ！"
        elif event.message.text == "部屋の電気けして！":
            GPIO.cleanup()
            subprocess.call(GREEN_SHELL, shell=True)
            text="部屋の電気を消したよ！" 

        elif event.message.text == "状況を教えて！":
            image_send_message()
            text="結果をHomeチャンネルに送信したよ！"

        elif event.message.text:
            text="そのメッセージには対応できないよ！"

    except Exception as e:
        print(e)

    print(text)
    linebot_api.reply_message(event.reply_token, TextSendMessage(text=text))


if __name__  == '__main__':
    app.run()


GPIO.cleanup()
cv2.destroyAllWindows()
# proc.terminate()