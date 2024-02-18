import RPi.GPIO as GPIO
import subprocess
import time
from flask import Flask, request, abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

CGIR_SEND = 19
RED_LED = 16
BLUE_LED = 20
GREEN_LED = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(CGIR_SEND, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

AC_ON_SHELL = "cgir send -c ./test_cgir.json -g19 AC_ON"
AC_OFF_SHELL = "cgir send -c ./test_cgir.json -g19 AC_OFF"
RED_SHELL = "cgir send -c ./test_cgir.json -g19 RED_LED"
BLUE_SHELL = "cgir send -c ./test_cgir.json -g19 BLUE_LED"
GREEN_SHELL = "cgir send -c ./test_cgir.json -g19 GREEN_LED"

app = Flask(__name__)
linebot_api = LineBotApi('')
handler = WebhookHandler('')

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
            GPIO.output(RED_LED, 1)
            subprocess.call(RED_SHELL, shell=True)
            text="LEDを「赤色」に変えたよ！"
        elif event.message.text == "青色にして！":
            GPIO.cleanup()
            GPIO.output(BLUE_LED, 1)
            subprocess.call(BLUE_SHELL, shell=True)
            text="LEDを「青色」に変えたよ！"
        elif event.message.text == "緑色にして！":
            GPIO.cleanup()
            GPIO.output(GREEN_LED, 1)
            subprocess.call(GREEN_SHELL, shell=True)
            text="LEDを「緑色」に変えたよ！"
    except Exception as e:
        print(e)

    if event.message.text == "状況を教えて！":
        if (GPIO.input(RED_LED) | GPIO.input(BLUE_LED) | GPIO.input(GREEN_LED)):
            if GPIO.input(RED_LED) == True:
                text="今は「赤色」のLEDが点いてるよ！"
            elif GPIO.input(BLUE_LED) == True:
                text="今は「青色」のLEDが点いてるよ！"
            elif GPIO.input(GREEN_LED) == True:
                text="今は「緑色」のLEDが点いてるよ！"
        else:
            text="今は何も点いていないよ！"

    print(text)
    linebot_api.reply_message(event.reply_token, TextSendMessage(text=text))

if __name__  == '__main__':
    app.run()