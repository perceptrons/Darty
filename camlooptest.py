import cv2 as cv
import numpy as np
import time
from matplotlib import pyplot as plt
import json
from picamera import PiCamera
from time import sleep

#from supportfunction import *
#from crop import *
camera = PiCamera()

camera.start_preview()
for i in range(5):
    sleep(10)
    camera.capture('ImageStart.png')
    print("yey")

camera.stop_preview()
