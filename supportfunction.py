from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv

def PiCamCapture(name):
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)

    #allow camera to warm up.
    time.sleep(0.1)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array

    #imwrite
    cv.imwrite(name,image)
    #display the image on screen and wait for a keypress
    #cv.imshow("Image", image)
    #cv.waitKey(0)
    return 0

def add_num(x,y):
    sum = x + y
    return sum
