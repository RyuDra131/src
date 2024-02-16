import cv2
from datetime import datetime
import numpy as np
import multiprocessing as mltp

now = datetime.now().strftime("%Y%mm%dd_%Hh%Mm%Ss")

# def ScanFace():
#     cam = cv2.VideoCapture(0)
#     while True:
#         ret,cap = cam.read()
#         key = cv2.waitKey(1)
#         cv2.imshow('frame', cap)
#         if(key == ord('s') | )

def FrontalFaces():
    try:
        frontal_face = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
        img = cv2.imread("./img/main.jpg")
        gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
        faces = frontal_face.detectMultiScale(gray, 1.1, 3, 0, (30,30))
        for(x, y, w, h) in faces:
            imgs = cv2.rectangle(img, (x, y), (x+w , y+h), (0, 0, 255), 3)
        cv2.imwrite(f"./img/capture/{now}.jpg", imgs)
        cv2.imshow('Face Detected', imgs)
    except UnboundLocalError:
        cv2.imshow('Not Found', img)

def FrontalCatFaces():
    try:
        frontal_catface = cv2.CascadeClassifier('./data/haarcascade_frontalcatface_extended.xml')
        img = cv2.imread("./img/cat.jpg")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        catfaces = frontal_catface.detectMultiScale(gray, minSize=(50,50))
        for(x, y, w, h) in catfaces:
            cat_imgs = cv2.rectangle(img, (x,y), (x+w , y+h), (255, 0, 255), 3)
        cv2.imwrite(f"./img/capture/{now}.jpg", cat_imgs)
        cv2.imshow('Catface', cat_imgs)
    except UnboundLocalError:
        cv2.imshow('Not Found', img)


def FrontalFaceGlasses():
    try:    
        eyeglasses = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
        img = cv2.imread("./img/test2.jpg")
        gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
        glasses = eyeglasses.detectMultiScale(gray, 1.1, 3, 0, (30,30))
        for(x, y, w, h) in glasses:
            imges = cv2.rectangle(img, (x, y), (x+w , y+h), (0, 0, 300), 4)
        cv2.imwrite(f"./img/capture/{now}.jpg", imges)
        cv2.imshow('Glasses' , imges)
    except UnboundLocalError:
        cv2.imshow('Not Found' , imges)

# FrontalFaces()
FrontalCatFaces()

cv2.waitKey(0)
cv2.destroyAllWindows()